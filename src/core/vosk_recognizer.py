"""
Vosk Speech Recognizer - Real-time, low-latency speech recognition
Latency: <1 second (vs 10-20s with Whisper)
"""

import json
import logging
import numpy as np
from typing import Optional
from pathlib import Path

from PySide6.QtCore import QObject, Signal, QThread

try:
    from vosk import Model, KaldiRecognizer
    import sounddevice as sd
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False
    Model = None
    KaldiRecognizer = None
    sd = None

logger = logging.getLogger(__name__)


class VoskAudioThread(QThread):
    """
    Hilo para captura continua de audio y procesamiento con Vosk.
    Latencia muy baja gracias a procesamiento incremental.
    """
    
    text_recognized = Signal(str)
    error_occurred = Signal(str)
    
    def __init__(self, recognizer, sample_rate: int = 16000):
        super().__init__()
        self.recognizer = recognizer
        self.sample_rate = sample_rate
        self.is_running = False
    
    def run(self):
        """Captura audio y procesa con Vosk en tiempo real"""
        if sd is None:
            self.error_occurred.emit("sounddevice no disponible")
            return
        
        self.is_running = True
        logger.info("Iniciando captura de audio con Vosk (tiempo real)")
        
        try:
            with sd.RawInputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype='int16',
                blocksize=4000  # ~250ms de audio
            ) as stream:
                
                while self.is_running:
                    # Leer chunk de audio
                    data, _ = stream.read(4000)
                    
                    # Procesar con Vosk (incremental)
                    if self.recognizer.AcceptWaveform(data.tobytes()):
                        # Frase completa detectada
                        result = json.loads(self.recognizer.Result())
                        if result.get('text'):
                            text = result['text'].strip()
                            logger.debug(f"Vosk texto: {text}")
                            self.text_recognized.emit(text)
                    else:
                        # Resultado parcial (opcional, para mostrar mientras habla)
                        partial = json.loads(self.recognizer.PartialResult())
                        if partial.get('partial'):
                            # Puedes emitir esto si quieres preview mientras habla
                            pass
        
        except Exception as e:
            logger.error(f"Error en captura de audio: {e}")
            self.error_occurred.emit(str(e))
        
        logger.info("Captura de audio detenida")
    
    def stop(self):
        """Detiene la captura de audio"""
        self.is_running = False


class VoskRecognizer(QObject):
    """
    Reconocedor de voz usando Vosk.
    Designed para latencia ultra-baja (<1 segundo).
    """
    
    # Señales para comunicación (compatibles con arquitectura existente)
    listening_started = Signal()
    listening_stopped = Signal()
    text_recognized = Signal(str)
    error_occurred = Signal(str)
    model_loaded = Signal()
    
    def __init__(self, model_path: str = None):
        super().__init__()
        
        if not VOSK_AVAILABLE:
            raise ImportError("Vosk no está instalado. Ejecuta: pip install vosk")
        
        # Configuración
        self.sample_rate = 16000
        self.is_listening = False
        self.model: Optional[Model] = None
        self.recognizer: Optional[KaldiRecognizer] = None
        self.audio_thread: Optional[VoskAudioThread] = None
        
        # Path al modelo
        if model_path is None:
            # Buscar modelo en directorio del proyecto
            model_path = Path(__file__).parent.parent.parent / "vosk-model-small-es-0.42"
        
        self.model_path = str(model_path)
        
        # Cargar modelo
        self._load_model()
    
    def _load_model(self):
        """Carga el modelo de Vosk"""
        try:
            logger.info(f"Cargando modelo Vosk desde: {self.model_path}")
            
            if not Path(self.model_path).exists():
                error_msg = f"Modelo no encontrado en: {self.model_path}"
                logger.error(error_msg)
                self.error_occurred.emit(error_msg)
                return
            
            # Cargar modelo (muy rápido, <1 segundo)
            self.model = Model(self.model_path)
            
            # Crear recognizer
            self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
            
            # Configurar para español
            self.recognizer.SetWords(True)  # Habilitar timestamps de palabras
            
            logger.info("Modelo Vosk cargado exitosamente")
            self.model_loaded.emit()
            
        except Exception as e:
            logger.error(f"Error cargando modelo Vosk: {e}")
            self.error_occurred.emit(f"Error cargando modelo: {str(e)}")
    
    def start_listening(self) -> bool:
        """
        Inicia el reconocimiento de voz en tiempo real.
        
        Returns:
            True si se inició correctamente
        """
        if self.is_listening:
            return True
        
        if self.model is None or self.recognizer is None:
            self.error_occurred.emit("Modelo no disponible")
            return False
        
        try:
            # Resetear recognizer
            self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
            self.recognizer.SetWords(True)
            
            # Iniciar hilo de captura
            self.audio_thread = VoskAudioThread(self.recognizer, self.sample_rate)
            self.audio_thread.text_recognized.connect(self.text_recognized.emit)
            self.audio_thread.error_occurred.connect(self._on_error)
            self.audio_thread.start()
            
            self.is_listening = True
            self.listening_started.emit()
            logger.info("Reconocimiento de voz Vosk iniciado")
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
            self.audio_thread.wait(2000)
            self.audio_thread = None
        
        self.listening_stopped.emit()
        logger.info("Reconocimiento de voz Vosk detenido")
    
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
    
    def _on_error(self, error: str):
        """Maneja errores del hilo de audio"""
        self.error_occurred.emit(error)
        self.stop_listening()
    
    def get_available_models(self) -> list:
        """Retorna lista de modelos disponibles (informativo)"""
        return ['vosk-model-small-es-0.42', 'vosk-model-es-0.42']
    
    def set_model(self, model_name: str) -> None:
        """Cambia el modelo (reinicia si está escuchando)"""
        was_listening = self.is_listening
        
        if was_listening:
            self.stop_listening()
        
        self.model_path = str(Path(__file__).parent.parent.parent / model_name)
        self._load_model()
        
        if was_listening and self.model is not None:
            self.start_listening()
