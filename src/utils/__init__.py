"""
Módulo de utilidades para Dictado por Voz
Contiene ConfigManager y ClipboardManager
"""

from .config import ConfigManager, config
from .clipboard import ClipboardManager

__all__ = ['ConfigManager', 'config', 'ClipboardManager']
