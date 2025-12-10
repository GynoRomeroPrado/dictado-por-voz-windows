"""
Dictado por Voz - Módulo principal
Aplicación de dictado por voz universal para Windows
"""

__version__ = "1.0.0"
__author__ = "Gyno Romero Prado"

from .utils import config, ConfigManager, ClipboardManager
from .core import HotkeyManager, CommandProcessor, SpeechRecognizer

__all__ = [
    'config',
    'ConfigManager',
    'ClipboardManager',
    'HotkeyManager',
    'CommandProcessor',
    'SpeechRecognizer',
]
