import os
import queue
import threading
import time
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

# Detección de Voz (Simple Energy VAD)
# Ajustado para ignorar ruido de fondo (400-500)
VAD_THRESHOLD = 600  
SILENCE_DURATION = 1.0  
MIN_RECORDING = 0.5     

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
        
        self.model_size = model_size
        self.model = None

    def start_listening(self):
        self.listening = True
        self.running = True
        
        # Carga síncrona (Bloquea UI unos segundos, pero es seguro)
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
            
        if self.on_status_change: self.on_status_change("Escuchando (Motor Listo)")

    def stop_listening(self):
        self.listening = False
        if self.on_status_change: self.on_status_change("Pausado")

    def run(self):
        """Main Audio Loop"""
        # Callbacks
        def audio_callback(indata, frames, time, status):
            if self.listening:
                self.audio_queue.put(indata.copy())

        # ==========================================
        # AUTO-CALIBRATION
        # ==========================================
        print("DEBUG: [Calibration] Measuring ambient noise...")
        ambient_samples = []
        with sd.InputStream(callback=audio_callback, channels=1, samplerate=16000, dtype='int16'):
            # Listen for 1.5 seconds
            start_cal = time.time()
            while time.time() - start_cal < 1.5:
                try:
                    if not self.audio_queue.empty():
                        chunk = self.audio_queue.get()
                        rms = np.sqrt(np.mean(chunk.flatten().astype(np.float64)**2))
                        ambient_samples.append(rms)
                except:
                    pass
        
        if ambient_samples:
            avg_noise = np.mean(ambient_samples)
            max_noise = np.max(ambient_samples)
            
            # Ajuste de Alta Sensibilidad: Solo +50 sobre el ruido
            # Minimo bajado a 250 para micromejoras
            global VAD_THRESHOLD
            VAD_THRESHOLD = max(max_noise + 50, 250)
            
            print(f"DEBUG: [Calibration] Noise Floor: {avg_noise:.2f} (Max: {max_noise:.2f})")
            print(f"DEBUG: [Calibration] New VAD Threshold: {VAD_THRESHOLD:.2f}")
            if self.on_status_change: 
                self.on_status_change(f"Calibrado Sensible (Umbral: {int(VAD_THRESHOLD)})")
        
        # Clear queue after calibration
        self.audio_queue.queue.clear()
        
        # ==========================================
        # MAIN LOOP
        # ==========================================
        print(f"DEBUG: Starting Main Loop with Threshold {VAD_THRESHOLD}")
        with sd.InputStream(callback=audio_callback, channels=1, samplerate=16000, dtype='int16'):
            while self.running:
                try:
                    chunk = self.audio_queue.get(timeout=0.5)
                    self.process_audio_chunk(chunk)
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Error loop: {e}")

    def process_audio_chunk(self, chunk):
        rms = np.sqrt(np.mean(chunk.flatten().astype(np.float64)**2))
        
        # DEBUG solo si es relevante (cerca del umbral)
        if rms > VAD_THRESHOLD * 0.8: 
            print(f"> Audio Level: {rms:.0f} (Thresh: {VAD_THRESHOLD:.0f})")

        if rms > VAD_THRESHOLD:
            if not self.is_voice_active:
                self.is_voice_active = True
                print("DEBUG: [VAD] Voice Started (Active)")
                if self.on_status_change: self.on_status_change("Detectando voz...")
            
            self.silence_start = None
            self.current_phrase.append(chunk)
            
        elif self.is_voice_active:
            # Silencio tras voz
            self.current_phrase.append(chunk)
            
            if self.silence_start is None:
                self.silence_start = time.time()
            
            # Verificar si excedimos el tiempo de silencio
            if time.time() - self.silence_start > SILENCE_DURATION:
                print("DEBUG: [VAD] Silence Timeout -> Transcribing")
                self.transcribe_phrase()
                self.is_voice_active = False
                self.current_phrase = []
                self.silence_start = None
                if self.on_status_change: self.on_status_change("Escuchando...")

    def transcribe_phrase(self):
        if not self.model or len(self.current_phrase) == 0:
            print("DEBUG: [Transcribe] No model or no audio")
            return

        full_audio_int16 = np.concatenate(self.current_phrase)
        audio_float32 = full_audio_int16.flatten().astype(np.float32) / 32768.0
        
        if len(audio_float32) < 16000 * MIN_RECORDING:
            print("DEBUG: [Transcribe] Audio too short")
            return

        try:
            print(f"DEBUG: [Transcribe] Starting Whisper on {len(audio_float32)/16000:.1f}s audio...")
            segments, _ = self.model.transcribe(
                audio_float32, 
                beam_size=5, 
                language="es",
                initial_prompt="Hola. Soy un asistente de dictado en español."
            )
            text = " ".join([segment.text for segment in segments]).strip()
            print(f"DEBUG: [Transcribe] Result: '{text}'")
            
            if text and self.on_text_recognized:
                print("DEBUG: [Callback] Sending text to UI/Keyboard")
                self.on_text_recognized(text)
            else:
                print("DEBUG: [Transcribe] Empty text result")
                
        except Exception as e:
            print(f"DEBUG: [Error] Transcribe failed: {e}")
