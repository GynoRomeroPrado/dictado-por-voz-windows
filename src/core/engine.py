import queue
import threading
import time
import numpy as np
import sounddevice as sd
import webrtcvad
from faster_whisper import WhisperModel

# Configuración VAD WebRTC
# Modo 0 (Muy permisivo) a 3 (Muy agresivo filtrando ruido)
VAD_MODE = 2 
SILENCE_DURATION = 0.6
MIN_RECORDING = 0.3

class VoiceEngine(threading.Thread):
    def __init__(self, model_size="small", on_text_recognized=None, on_status_change=None):
        super().__init__()
        self.daemon = True
        self.running = False
        self.listening = False
        self.on_text_recognized = on_text_recognized
        self.on_status_change = on_status_change
        
        # Audio buffer
        self.audio_queue = queue.Queue()
        self.current_phrase = []
        self.silence_start = None
        self.is_voice_active = False
        
        # WebRTC VAD
        try:
            self.vad = webrtcvad.Vad(VAD_MODE)
            print(f"WebRTC VAD Initialized in Mode {VAD_MODE}")
        except Exception as e:
            print(f"Error init WebRTC VAD: {e}")
            self.vad = None
        
        # Whisper Model
        self.model_size = model_size
        self.model = None

    def start_listening(self):
        self.listening = True
        self.running = True
        
        # Carga Whisper
        if not self.model:
            try:
                if self.on_status_change: self.on_status_change("Cargando Whisper (Espere)...")
                self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
                print("Whisper model loaded.")
            except Exception as e:
                print(f"Error loading model: {e}")
                if self.on_status_change: self.on_status_change(f"Error: {e}")
                return

        if not self.is_alive():
            self.start()
            
        if self.on_status_change: self.on_status_change("Escuchando (VAD WebRTC)")

    def stop_listening(self):
        self.listening = False
        if self.on_status_change: self.on_status_change("Pausado")

    def run(self):
        """Main Audio Loop"""
        def audio_callback(indata, frames, time, status):
            if self.listening:
                self.audio_queue.put(indata.copy())

        # IMPORTANT: WebRTC works on 10/20/30ms frames.
        # 16000 Hz * 0.030 s = 480 samples.
        # We enforce blocksize=480 to feed valid frames directly.
        with sd.InputStream(callback=audio_callback, channels=1, samplerate=16000, blocksize=480, dtype='int16'):
            while self.running:
                try:
                    chunk = self.audio_queue.get(timeout=0.5)
                    self.process_audio_chunk(chunk)
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Error loop: {e}")

    def process_audio_chunk(self, chunk):
        if not self.vad:
            return 

        # WebRTC expects raw bytes
        is_speech = self.vad.is_speech(chunk.tobytes(), 16000)
        
        if is_speech:
            if not self.is_voice_active:
                self.is_voice_active = True
                print("DEBUG: [WebRTC] Voice Start")
                if self.on_status_change: self.on_status_change("Voz detectada...")
            
            self.silence_start = None
            self.current_phrase.append(chunk)
            
        elif self.is_voice_active:
            # Silencio tras voz
            self.current_phrase.append(chunk)
            
            if self.silence_start is None:
                self.silence_start = time.time()
            
            # Verificar si excedimos el tiempo de silencio
            if time.time() - self.silence_start > SILENCE_DURATION:
                print("DEBUG: [WebRTC] Silence detected -> Transcribing")
                self.transcribe_phrase()
                self.is_voice_active = False
                self.current_phrase = []
                self.silence_start = None
                if self.on_status_change: self.on_status_change("Escuchando...")

    def transcribe_phrase(self):
        if not self.model or len(self.current_phrase) == 0:
            return

        full_audio_int16 = np.concatenate(self.current_phrase)
        audio_float32 = full_audio_int16.flatten().astype(np.float32) / 32768.0
        
        if len(audio_float32) < 16000 * MIN_RECORDING:
            return

        try:
            print(f"DEBUG: Transcribing {len(audio_float32)/16000:.2f}s...")
            segments, _ = self.model.transcribe(
                audio_float32, 
                beam_size=5, 
                language="es", 
                initial_prompt="Hola. Soy un asistente de dictado."
            )
            text = " ".join([segment.text for segment in segments]).strip()
            
            # Filtro anti-alucinación
            hallucination_trigger = "Soy un asistente de dictado"
            if not text or len(text) < 2 or hallucination_trigger.lower() in text.lower():
                print(f"Ignored hallucination: {text}")
                return

            print(f"Recognized: {text}")
            if self.on_text_recognized:
                self.on_text_recognized(text)
                
        except Exception as e:
            print(f"Transcribe error: {e}")
