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
            sample_rate: Frecuencia de muestreo (RNNoise espera 48kHz internamente)
        """
        self.sample_rate = sample_rate
        self.denoiser = None
        self.enabled = False
        
        if RNNOISE_AVAILABLE:
            try:
                # RNNoise trabaja a 48kHz internamente
                self.denoiser = pyrnnoise.RNNoise()
                self.enabled = True
                logger.info("Cancelación de ruido RNNoise inicializada")
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
            # RNNoise espera audio a 48kHz, 16-bit PCM
            # Nuestro audio está a 16kHz, necesitamos resamplear
            
            # Convertir de float32 [-1,1] a int16
            audio_int16 = (audio * 32767).astype(np.int16)
            
            # RNNoise procesa en frames de 480 muestras (10ms a 48kHz)
            # Como estamos a 16kHz, procesamos en frames de 160 muestras
            frame_size = 160  # 10ms a 16kHz
            
            # Padding para que sea múltiplo del frame_size
            original_length = len(audio_int16)
            padded_length = ((original_length + frame_size - 1) // frame_size) * frame_size
            if padded_length > original_length:
                audio_int16 = np.pad(audio_int16, (0, padded_length - original_length))
            
            # Procesar cada frame
            output_frames = []
            for i in range(0, len(audio_int16), frame_size):
                frame = audio_int16[i:i+frame_size].tobytes()
                # RNNoise procesa y retorna el frame filtrado
                filtered = self.denoiser.process_frame(frame)
                output_frames.append(np.frombuffer(filtered, dtype=np.int16))
            
            # Concatenar frames
            output = np.concatenate(output_frames)
            
            # Recortar al tamaño original
            output = output[:original_length]
            
            # Convertir de int16 a float32 [-1, 1]
            output_float = output.astype(np.float32) / 32767.0
            
            return output_float
            
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
