"""
Sistema de bandeja simplificado para dictado por voz
Solo icono en bandeja del sistema, sin ventana principal
"""

from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QObject, Signal

try:
    from ..utils.config import config
except ImportError:
    from utils.config import config


class TrayIcon(QObject):
    """Icono de bandeja del sistema minimalista"""

    # Signals
    toggle_dictation_signal = Signal()
    open_settings_signal = Signal()
    quit_signal = Signal()

    def __init__(self):
        """Initialize tray icon"""
        super().__init__()

        self.is_listening = False
        self.tray_icon = None
        self.setup_tray()

    def setup_tray(self):
        """Setup system tray icon"""
        # Create tray icon
        self.tray_icon = QSystemTrayIcon(self)

        # TODO: Add custom icon
        # For now, using system default
        # self.tray_icon.setIcon(QIcon('path/to/icon.png'))

        # Create menu
        menu = QMenu()

        # Status label
        self.status_action = QAction("🔴 Detenido", self)
        self.status_action.setEnabled(False)
        menu.addAction(self.status_action)

        menu.addSeparator()

        # Toggle dictation
        toggle_action = QAction("Iniciar/Detener Dictado", self)
        toggle_action.triggered.connect(self.toggle_dictation_signal.emit)
        menu.addAction(toggle_action)

        menu.addSeparator()

        # Settings
        settings_action = QAction("⚙ Configuración", self)
        settings_action.triggered.connect(self.open_settings_signal.emit)
        menu.addAction(settings_action)

        # Quit
        quit_action = QAction("Salir", self)
        quit_action.triggered.connect(self.quit_signal.emit)
        menu.addAction(quit_action)

        self.tray_icon.setContextMenu(menu)

        # Show tray icon
        self.tray_icon.show()

        # Set tooltip
        self.update_tooltip()

    def set_listening_state(self, is_listening: bool):
        """
        Update tray icon based on listening state

        Args:
            is_listening: True if currently listening
        """
        self.is_listening = is_listening

        if is_listening:
            self.status_action.setText("🔴 Escuchando...")
            # TODO: Change icon to indicate listening
        else:
            self.status_action.setText("⚫ Detenido")
            # TODO: Change icon to indicate stopped

        self.update_tooltip()

    def update_tooltip(self):
        """Update tooltip text"""
        if self.is_listening:
            tooltip = "Dictado por Voz - Escuchando\nHabla ahora..."
        else:
            hotkey = config.get('hotkeys.toggle_dictation', 'Ctrl+Shift+Space')
            tooltip = f"Dictado por Voz - Detenido\nPresiona {hotkey} para iniciar"

        self.tray_icon.setToolTip(tooltip)

    def show_notification(self, title: str, message: str, duration: int = 2000):
        """
        Show system notification

        Args:
            title: Notification title
            message: Notification message
            duration: Duration in milliseconds
        """
        if config.get('ui.show_notifications', True):
            self.tray_icon.showMessage(
                title,
                message,
                QSystemTrayIcon.MessageIcon.Information,
                duration
            )

    def hide(self):
        """Hide tray icon"""
        if self.tray_icon:
            self.tray_icon.hide()

    def show(self):
        """Show tray icon"""
        if self.tray_icon:
            self.tray_icon.show()
