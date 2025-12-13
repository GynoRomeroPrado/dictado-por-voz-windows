"""
audio_preprocessor.py - Preprocesamiento de audio con cancelación de ruido
Utiliza RNNoise para eliminar ruido de fondo (ventiladores, aire acondicionado, etc.)
antes de enviar el audio a Whisper.
"""

import numpy as np
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Intentar importar RNNoise
try:
    import pyrnnoise
    RNNOISE_AVAILABLE = True
    logger.info("RNNoise disponible para cancelación de ruido")
except ImportError:
    RNNOISE_AVAILABLE = False
    logger.warning("RNNoise no disponible - sin cancelación de ruido")


class AudioPreprocessor:
    """
    Preprocesador de audio que aplica cancelación de ruido antes de transcripción.
    
    RNNoise está entrenado específicamente para eliminar ruido de fondo
    mientras preserva la voz humana, perfecto para micrófonos en ambientes ruidosos.
    """
    
    def __init__(self, sample_rate: int = 16000):
        """
        Inicializa el preprocesador.
        
        Args:
            sample_rate: Frecuencia de muestreo del audio
        """
        self.sample_rate = sample_rate
        self.denoiser = None
        self.enabled = False
        
        if RNNOISE_AVAILABLE:
            try:
                # Inicializar RNNoise con sample_rate correcto
                self.denoiser = pyrnnoise.RNNoise(sample_rate=sample_rate)
                self.enabled = True
                logger.info(f"Cancelación de ruido RNNoise inicializada ({sample_rate}Hz)")
            except Exception as e:
                logger.error(f"Error inicializando RNNoise: {e}")
                self.enabled = False
    
    def process(self, audio: np.ndarray) -> np.ndarray:
        """
        Aplica cancelación de ruido al audio.
        
        Args:
            audio: Array de audio float32 normalizado [-1, 1]
            
        Returns:
            Audio procesado con ruido reducido
        """
        if not self.enabled or self.denoiser is None:
            return audio
        
        try:
            # pyrnnoise espera float32 y retorna float32
            # Asegurar que el audio sea 1D y float32
            audio_1d = audio.flatten().astype(np.float32)
            
            # Aplicar cancelación de ruido
            denoised = self.denoiser.denoise_wav(audio_1d)
            
            return denoised
            
        except Exception as e:
            logger.warning(f"Error en cancelación de ruido: {e}, usando audio original")
            return audio
    
    def set_enabled(self, enabled: bool):
        """Activa o desactiva la cancelación de ruido."""
        if RNNOISE_AVAILABLE and self.denoiser:
            self.enabled = enabled
            logger.info(f"Cancelación de ruido: {'activada' if enabled else 'desactivada'}")
    
    def is_available(self) -> bool:
        """Retorna True si RNNoise está disponible."""
        return RNNOISE_AVAILABLE and self.denoiser is not None


# Singleton global para uso fácil
_preprocessor: Optional[AudioPreprocessor] = None


def get_preprocessor() -> AudioPreprocessor:
    """Obtiene el preprocesador singleton."""
    global _preprocessor
    if _preprocessor is None:
        _preprocessor = AudioPreprocessor()
    return _preprocessor


def denoise_audio(audio: np.ndarray) -> np.ndarray:
    """
    Función de conveniencia para aplicar cancelación de ruido.
    
    Args:
        audio: Array numpy float32 normalizado
        
    Returns:
        Audio con ruido reducido
    """
    return get_preprocessor().process(audio)
