"""
Hybrid Recognizer - Sistema dual para mejor UX
Vosk (rápido) + Whisper (preciso)
"""

import logging
from typing import Optional
from PySide6.QtCore import QObject, Signal

from .vosk_recognizer import VoskRecognizer, VOSK_AVAILABLE
from .speech_recognizer import SpeechRecognizer

logger = logging.getLogger(__name__)


class HybridRecognizer(QObject):
    """
    Reconocedor híbrido que usa Vosk para respuesta inmediata
    y Whisper para corrección precisa en background.
    """
    
    # Señales unificadas
    listening_started = Signal()
    listening_stopped = Signal()
    text_recognized = Signal(str)  # Texto de Vosk (rápido)
    text_corrected = Signal(str)   # Texto de Whisper (preciso) 
    error_occurred = Signal(str)
    model_loaded = Signal()
    
    def __init__(self):
        super().__init__()
        
        self.is_listening = False
        self._vosk = None
        self._whisper = None
        
        # Inicializar motores
        try:
            if VOSK_AVAILABLE:
                self._vosk = VoskRecognizer()
                self._vosk.text_recognized.connect(self._on_vosk_text)
                self._vosk.error_occurred.connect(self.error_occurred.emit)
                logger.info("Vosk inicializado (respuesta rápida)")
            
            self._whisper = SpeechRecognizer()
            self._whisper.text_recognized.connect(self._on_whisper_text)
            self._whisper.error_occurred.connect(self.error_occurred.emit)
            logger.info("Whisper inicializado (alta precisión)")
            
            self.model_loaded.emit()
            
        except Exception as e:
            logger.error(f"Error inicializando reconocedores: {e}")
            self.error_occurred.emit(str(e))
    
    def start_listening(self) -> bool:
        """Inicia ambos motores de reconocimiento"""
        if self.is_listening:
            return True
        
        success = True
        
        # Iniciar Vosk primero (inmediato)
        if self._vosk:
            if not self._vosk.start_listening():
                logger.warning("Vosk no pudo iniciar, solo usando Whisper")
                success = False
        
        # Iniciar Whisper (background)
        if self._whisper:
            if not self._whisper.start_listening():
                logger.error("Whisper no pudo iniciar")
                if self._vosk:
                    self._vosk.stop_listening()
                return False
        
        if success or self._whisper.is_listening:
            self.is_listening = True
            self.listening_started.emit()
            logger.info("Sistema híbrido iniciado")
            return True
        
        return False
    
    def stop_listening(self) -> None:
        """Detiene ambos motores"""
        if not self.is_listening:
            return
        
        if self._vosk:
            self._vosk.stop_listening()
        
        if self._whisper:
            self._whisper.stop_listening()
        
        self.is_listening = False
        self.listening_stopped.emit()
        logger.info("Sistema híbrido detenido")
    
    def toggle_listening(self) -> bool:
        """Alterna estado de escucha"""
        if self.is_listening:
            self.stop_listening()
            return False
        else:
            return self.start_listening()
    
    def _on_vosk_text(self, text: str):
        """Callback de Vosk - resultado preliminar rápido"""
        logger.debug(f"Vosk (preliminar): {text}")
        self.text_recognized.emit(text)
    
    def _on_whisper_text(self, text: str):
        """Callback de Whisper - resultado final preciso"""
        logger.debug(f"Whisper (corregido): {text}")
        self.text_corrected.emit(text)
    
    def get_available_models(self) -> list:
        """Retorna modelos disponibles de Whisper"""
        if self._whisper:
            return self._whisper.get_available_models()
        return []
    
    def set_model(self, model_name: str) -> None:
        """Cambia modelo de Whisper"""
        if self._whisper:
            self._whisper.set_model(model_name)
