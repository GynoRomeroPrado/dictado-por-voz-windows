"""
SpeechRecognizer - Motor de reconocimiento de voz con Whisper
Utiliza faster-whisper para reconocimiento local y Silero VAD para detección de voz
"""

import logging
import threading
import queue
import time
import os
from pathlib import Path
from typing import Optional, Callable

import numpy as np

try:
    import sounddevice as sd
except ImportError:
    sd = None

try:
    from faster_whisper import WhisperModel
except ImportError:
    WhisperModel = None

try:
    import onnxruntime as ort
except ImportError:
    ort = None

from PySide6.QtCore import QObject, Signal, QThread

from ..utils.config import config

logger = logging.getLogger(__name__)


class SileroVAD:
    """
    Voice Activity Detection usando Silero VAD con ONNX Runtime.
    Detecta cuando el usuario está hablando para optimizar el reconocimiento.
    """
    
    def __init__(self, model_path: Optional[str] = None, threshold: float = 0.5):
        """
        Inicializa Silero VAD.
        
        Args:
            model_path: Ruta al modelo ONNX (por defecto busca silero_vad.onnx)
            threshold: Umbral de detección de voz (0.0-1.0)
        """
        self.threshold = threshold
        self.sample_rate = 16000
        self._h = np.zeros((2, 1, 64), dtype=np.float32)
        self._c = np.zeros((2, 1, 64), dtype=np.float32)
        self.session: Optional[ort.InferenceSession] = None
        
        if ort is None:
            logger.warning("ONNX Runtime no disponible, VAD desactivado")
            return
        
        # Buscar modelo VAD
        if model_path is None:
            # Buscar en ubicaciones comunes
            base_dir = Path(__file__).parent.parent.parent
            possible_paths = [
                base_dir / 'silero_vad.onnx',
                base_dir / 'assets' / 'silero_vad.onnx',
                base_dir / 'src' / 'assets' / 'silero_vad.onnx',
            ]
            for path in possible_paths:
                if path.exists():
                    model_path = str(path)
                    break
        
        if model_path and os.path.exists(model_path):
            try:
                self.session = ort.InferenceSession(
                    model_path,
                    providers=['CPUExecutionProvider']
                )
                logger.info(f"Silero VAD cargado desde: {model_path}")
            except Exception as e:
                logger.error(f"Error cargando Silero VAD: {e}")
        else:
            logger.warning(f"Modelo VAD no encontrado")
    
    def is_speech(self, audio_chunk: np.ndarray) -> bool:
        """
        Detecta si el chunk de audio contiene voz.
        
        Args:
            audio_chunk: Array de audio float32 normalizado
            
        Returns:
            True si se detecta voz
        """
        if self.session is None:
            return True  # Sin VAD, asumir que siempre hay voz
        
        try:
            # Preparar input para el modelo
            audio = audio_chunk.astype(np.float32)
            if len(audio.shape) == 1:
                audio = audio.reshape(1, -1)
            
            # Asegurar longitud correcta (512 samples para 16kHz)
            if audio.shape[1] < 512:
                audio = np.pad(audio, ((0, 0), (0, 512 - audio.shape[1])))
            elif audio.shape[1] > 512:
                audio = audio[:, :512]
            
            # Ejecutar inferencia
            sr = np.array([self.sample_rate], dtype=np.int64)
            ort_inputs = {
                'input': audio,
                'sr': sr,
                'h': self._h,
                'c': self._c
            }
            
            ort_outputs = self.session.run(None, ort_inputs)
            out, self._h, self._c = ort_outputs
            
            probability = out[0][0]
            return float(probability) > self.threshold
            
        except Exception as e:
            logger.debug(f"Error en VAD: {e}")
            return True
    
    def reset_states(self) -> None:
        """Reinicia los estados internos del modelo"""
        self._h = np.zeros((2, 1, 64), dtype=np.float32)
        self._c = np.zeros((2, 1, 64), dtype=np.float32)


class AudioRecorderThread(QThread):
    """
    Hilo para captura continua de audio del micrófono.
    Envía chunks cada 3 segundos máximo para baja latencia.
    """
    
    audio_ready = Signal(np.ndarray)
    error_occurred = Signal(str)
    
    # Configuración de tiempos (OPTIMIZADO para latencia ULTRA baja)
    MAX_CHUNK_DURATION = 2.0      # Procesar cada 2 segundos máximo (REDUCIDO)
    MIN_CHUNK_DURATION = 0.5      # Mínimo de audio para procesar  
    SILENCE_THRESHOLD = 0.5       # Reducido para procesar más rápido
    
    def __init__(self, sample_rate: int = 16000):
        super().__init__()
        self.sample_rate = sample_rate
        self.is_running = False
        self.vad = SileroVAD()
        
        # Calcular límites en muestras
        self._max_samples = int(sample_rate * self.MAX_CHUNK_DURATION)
        self._min_samples = int(sample_rate * self.MIN_CHUNK_DURATION)
        self._silence_samples_threshold = int(sample_rate * self.SILENCE_THRESHOLD)
    
    def run(self):
        """Ejecuta la captura de audio con envío periódico"""
        if sd is None:
            self.error_occurred.emit("sounddevice no disponible")
            return
        
        self.is_running = True
        logger.info("Iniciando captura de audio (chunks cada 2.5s)")
        
        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype='float32',
                blocksize=512
            ) as stream:
                
                audio_buffer = []
                total_samples = 0
                silence_samples = 0
                last_emit_time = time.time()
                
                while self.is_running:
                    data, _ = stream.read(512)
                    audio_chunk = data.flatten()
                    chunk_samples = len(audio_chunk)
                    
                    # Detectar voz
                    is_speech = self.vad.is_speech(audio_chunk)
                    
                    if is_speech:
                        # Hay voz: acumular
                        audio_buffer.append(audio_chunk)
                        total_samples += chunk_samples
                        silence_samples = 0
                    else:
                        # Silencio
                        silence_samples += chunk_samples
                        
                        # Seguir acumulando silencio corto (para contexto)
                        if audio_buffer and silence_samples < self._silence_samples_threshold:
                            audio_buffer.append(audio_chunk)
                            total_samples += chunk_samples
                    
                    # Calcular tiempo transcurrido
                    current_time = time.time()
                    time_elapsed = current_time - last_emit_time
                    
                    # Decidir si enviar
                    should_send = False
                    
                    if audio_buffer and total_samples >= self._min_samples:
                        # Enviar si:
                        # 1. Detectamos silencio suficiente, O
                        # 2. Han pasado 3 segundos, O
                        # 3. Buffer muy largo (seguridad)
                        
                        silence_detected = silence_samples >= self._silence_samples_threshold
                        time_limit_reached = time_elapsed >= self.MAX_CHUNK_DURATION
                        buffer_overflow = total_samples >= self._max_samples * 2
                        
                        should_send = silence_detected or time_limit_reached or buffer_overflow
                    
                    if should_send:
                        # Concatenar y enviar
                        full_audio = np.concatenate(audio_buffer)
                        duration_secs = len(full_audio) / self.sample_rate
                        
                        logger.debug(f"Enviando chunk: {duration_secs:.1f}s de audio")
                        self.audio_ready.emit(full_audio)
                        
                        # Reset
                        audio_buffer = []
                        total_samples = 0
                        silence_samples = 0
                        last_emit_time = current_time
                        self.vad.reset_states()
        
        except Exception as e:
            self.error_occurred.emit(f"Error de audio: {str(e)}")
            logger.error(f"Error en captura de audio: {e}")
        
        logger.info("Captura de audio detenida")
    
    def stop(self):
        """Detiene la captura de audio"""
        self.is_running = False


class SpeechRecognizer(QObject):
    """
    Motor de reconocimiento de voz usando faster-whisper.
    Proporciona reconocimiento en tiempo real con VAD.
    """
    
    # Señales Qt para comunicación con la UI
    text_recognized = Signal(str)
    listening_started = Signal()
    listening_stopped = Signal()
    error_occurred = Signal(str)
    
    def __init__(self):
        super().__init__()
        
        # Configuración
        self.language = config.get('language', 'es-PE')
        self.model_name = config.get('recognition.model', 'medium')
        
        # Estado
        self.is_listening = False
        self.model: Optional[WhisperModel] = None
        self.audio_thread: Optional[AudioRecorderThread] = None
        
        # Cargar modelo en segundo plano
        self._load_model_async()
    
    def _load_model_async(self) -> None:
        """Carga el modelo Whisper en un hilo separado"""
        def load():
            self._load_model()
        
        thread = threading.Thread(target=load, daemon=True)
        thread.start()
    
    def _load_model(self) -> None:
        """Carga el modelo Whisper"""
        if WhisperModel is None:
            logger.error("faster-whisper no está instalado")
            self.error_occurred.emit("faster-whisper no disponible")
            return
        
        try:
            # Determinar dispositivo (CUDA si disponible, sino CPU)
            device = "cuda" if self._is_cuda_available() else "cpu"
            compute_type = "float16" if device == "cuda" else "int8"
            
            logger.info(f"Cargando modelo Whisper '{self.model_name}' en {device}")
            
            self.model = WhisperModel(
                self.model_name,
                device=device,
                compute_type=compute_type
            )
            
            logger.info(f"Modelo Whisper cargado exitosamente")
            
        except Exception as e:
            logger.error(f"Error cargando modelo Whisper: {e}")
            self.error_occurred.emit(f"Error cargando modelo: {str(e)}")
    
    def _is_cuda_available(self) -> bool:
        """Verifica si CUDA está disponible"""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False
    
    def start_listening(self) -> bool:
        """
        Inicia el reconocimiento de voz.
        
        Returns:
            True si se inició correctamente
        """
        if self.is_listening:
            return True
        
        if self.model is None:
            # Intentar cargar modelo síncronamente
            self._load_model()
            if self.model is None:
                self.error_occurred.emit("Modelo no disponible")
                return False
        
        try:
            # Iniciar hilo de captura de audio
            self.audio_thread = AudioRecorderThread()
            self.audio_thread.audio_ready.connect(self._on_audio_ready)
            self.audio_thread.error_occurred.connect(self._on_audio_error)
            self.audio_thread.start()
            
            self.is_listening = True
            self.listening_started.emit()
            logger.info("Reconocimiento de voz iniciado")
            return True
            
        except Exception as e:
            logger.error(f"Error iniciando reconocimiento: {e}")
            self.error_occurred.emit(str(e))
            return False
    
    def stop_listening(self) -> None:
        """Detiene el reconocimiento de voz"""
        if not self.is_listening:
            return
        
        self.is_listening = False
        
        if self.audio_thread:
            self.audio_thread.stop()
            self.audio_thread.wait(2000)  # Esperar máximo 2 segundos
            self.audio_thread = None
        
        self.listening_stopped.emit()
        logger.info("Reconocimiento de voz detenido")
    
    def toggle_listening(self) -> bool:
        """
        Alterna el estado de escucha.
        
        Returns:
            True si ahora está escuchando
        """
        if self.is_listening:
            self.stop_listening()
            return False
        else:
            return self.start_listening()
    
    def _on_audio_ready(self, audio: np.ndarray) -> None:
        """
        Callback cuando hay audio listo para transcribir.
        Ejecuta la transcripción en un hilo separado para no bloquear la UI.
        
        Args:
            audio: Array de audio capturado
        """
        if not self.is_listening or self.model is None:
            return
        
        # Ejecutar transcripción en hilo separado para no bloquear UI
        def transcribe_async():
            try:
                # Extraer código de idioma (ej: 'es' de 'es-PE')
                lang_code = self.language.split('-')[0] if '-' in self.language else self.language
                
                # Transcribir con Whisper (BALANCE precisión/velocidad + puntuación)
                segments, info = self.model.transcribe(
                    audio,
                    language=lang_code,
                    beam_size=3,
                    best_of=1,
                    temperature=0.0,
                    vad_filter=True,
                    vad_parameters=dict(
                        min_silence_duration_ms=500,  # Aumentado: requiere más silencio
                        speech_pad_ms=100,            # Reducido: menos padding
                        threshold=0.6                 # AUMENTADO: filtra mejor ruido de fondo
                    ),
                    word_timestamps=False,
                    condition_on_previous_text=False
                )
                
                # Concatenar segmentos
                text_parts = []
                for segment in segments:
                    text = segment.text.strip()
                    if text:
                        text_parts.append(text)
                
                full_text = ' '.join(text_parts).strip()
                
                # FILTRO: Ignorar textos basura comunes de Whisper
                garbage_phrases = [
                    "transcripción",
                    "español latinoamericano",
                    "subtítulos",
                    "amara.org",
                    "suscríbete",
                    "gracias por ver",
                    "thanks for watching",
                    "subscribe",
                    "comunidad de amara"
                ]
                
                # Verificar si contiene frases basura
                if full_text:
                    text_lower = full_text.lower()
                    is_garbage = any(phrase in text_lower for phrase in garbage_phrases)
                    
                    if not is_garbage and self.is_listening:
                        logger.debug(f"Texto reconocido: {full_text}")
                        self.text_recognized.emit(full_text)
                    elif is_garbage:
                        logger.debug(f"Texto ignorado (basura): {full_text}")
                    
            except Exception as e:
                logger.error(f"Error en transcripción: {e}")
        
        # Iniciar transcripción en hilo separado
        thread = threading.Thread(target=transcribe_async, daemon=True)
        thread.start()
    
    def _on_audio_error(self, error: str) -> None:
        """Callback para errores de audio"""
        self.error_occurred.emit(error)
        self.stop_listening()
    
    def get_available_models(self) -> list:
        """Retorna lista de modelos disponibles"""
        return ['tiny', 'base', 'small', 'medium', 'large-v3', 'large-v3-turbo']
    
    def set_model(self, model_name: str) -> None:
        """
        Cambia el modelo de reconocimiento.
        
        Args:
            model_name: Nombre del modelo a usar
        """
        if model_name != self.model_name:
            self.model_name = model_name
            config.set('recognition.model', model_name)
            
            # Recargar modelo
            was_listening = self.is_listening
            if was_listening:
                self.stop_listening()
            
            self.model = None
            self._load_model_async()
            
            if was_listening:
                # Esperar un poco y reiniciar
                threading.Timer(2.0, self.start_listening).start()
    
    def set_language(self, language: str) -> None:
        """
        Cambia el idioma de reconocimiento.
        
        Args:
            language: Código de idioma (ej: 'es-MX', 'en-US')
        """
        self.language = language
        config.set('language', language)
        logger.info(f"Idioma cambiado a: {language}")
