"""
Módulo core para Dictado por Voz
Contiene la lógica principal de reconocimiento y procesamiento
"""

from .hotkey_manager import HotkeyManager
from .command_processor import CommandProcessor
from .speech_recognizer import SpeechRecognizer

__all__ = ['HotkeyManager', 'CommandProcessor', 'SpeechRecognizer']
