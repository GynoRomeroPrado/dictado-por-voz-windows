"""
Módulo UI para Dictado por Voz
Contiene la interfaz gráfica con PySide6
"""

from .main_window import MainWindow
from .settings_dialog import SettingsDialog
from .system_tray import SystemTrayIcon
from .floating_widget import FloatingWidgetManager, FloatingMicButton, TextOverlay

__all__ = ['MainWindow', 'SettingsDialog', 'SystemTrayIcon', 'FloatingWidgetManager', 'FloatingMicButton', 'TextOverlay']
