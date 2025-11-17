"""
Sistema de bandeja simplificado para dictado por voz
Solo icono en bandeja del sistema, sin ventana principal
"""

from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QObject, Signal

try:
    from ..utils.config import config
    from ..utils.auto_start import AutoStart
except ImportError:
    from utils.config import config
    from utils.auto_start import AutoStart


class TrayIcon(QObject):
    """Icono de bandeja del sistema minimalista"""

    # Signals
    toggle_dictation_signal = Signal()
    open_settings_signal = Signal()
    open_quick_settings_signal = Signal()
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

        # === STATUS ===
        self.status_action = QAction("⚫ Detenido", self)
        self.status_action.setEnabled(False)
        menu.addAction(self.status_action)

        menu.addSeparator()

        # === MAIN ACTIONS ===
        # Toggle dictation (BOLD - acción principal)
        toggle_action = QAction("▶ Iniciar/Detener Dictado", self)
        font = toggle_action.font()
        font.setBold(True)
        toggle_action.setFont(font)
        toggle_action.triggered.connect(self.toggle_dictation_signal.emit)
        menu.addAction(toggle_action)

        menu.addSeparator()

        # === QUICK ACCESS ===
        # Quick settings
        quick_settings_action = QAction("⚙ Configuración Rápida...", self)
        quick_settings_action.triggered.connect(self.open_quick_settings_signal.emit)
        menu.addAction(quick_settings_action)

        # Auto-start toggle
        self.autostart_action = QAction("🚀 Iniciar con Windows", self)
        self.autostart_action.setCheckable(True)
        self.autostart_action.setChecked(AutoStart.is_enabled())
        self.autostart_action.triggered.connect(self.toggle_autostart)
        menu.addAction(self.autostart_action)

        menu.addSeparator()

        # === LANGUAGE QUICK MENU ===
        language_menu = QMenu("🌍 Idioma Rápido", menu)

        languages = [
            ('es-ES', '🇪🇸 Español'),
            ('en-US', '🇺🇸 English'),
            ('fr-FR', '🇫🇷 Français'),
            ('de-DE', '🇩🇪 Deutsch'),
        ]

        current_lang = config.get('language', 'es-ES')
        for lang_code, lang_name in languages:
            lang_action = QAction(lang_name, self)
            lang_action.setCheckable(True)
            lang_action.setChecked(lang_code == current_lang)
            lang_action.triggered.connect(
                lambda checked, code=lang_code: self.change_language(code)
            )
            language_menu.addAction(lang_action)

        menu.addMenu(language_menu)

        menu.addSeparator()

        # === ADVANCED ===
        # Full settings
        settings_action = QAction("⚙ Configuración Avanzada...", self)
        settings_action.triggered.connect(self.open_settings_signal.emit)
        menu.addAction(settings_action)

        # === QUIT ===
        quit_action = QAction("❌ Salir", self)
        quit_action.triggered.connect(self.quit_signal.emit)
        menu.addAction(quit_action)

        # Set context menu
        self.tray_icon.setContextMenu(menu)

        # Double-click to toggle dictation
        self.tray_icon.activated.connect(self.on_icon_activated)

        # Show tray icon
        self.tray_icon.show()

        # Set tooltip
        self.update_tooltip()

    def on_icon_activated(self, reason):
        """Handle tray icon activation (click/double-click)"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            # Double-click toggles dictation
            self.toggle_dictation_signal.emit()

    def toggle_autostart(self, checked):
        """Toggle auto-start with Windows"""
        try:
            if checked:
                success = AutoStart.enable()
                if not success:
                    self.autostart_action.setChecked(False)
                    self.show_notification(
                        "Error",
                        "No se pudo habilitar auto-inicio.\nEjecuta como Administrador."
                    )
            else:
                AutoStart.disable()

            # Update checkbox to reflect actual state
            self.autostart_action.setChecked(AutoStart.is_enabled())

        except Exception as e:
            self.autostart_action.setChecked(AutoStart.is_enabled())
            self.show_notification("Error", f"Error al cambiar auto-inicio: {e}")

    def change_language(self, language_code):
        """Change language quickly from menu"""
        try:
            config.set('language', language_code)
            self.show_notification(
                "Idioma Cambiado",
                f"Idioma cambiado a: {language_code}\nReinicia para aplicar cambios."
            )
        except Exception as e:
            self.show_notification("Error", f"Error cambiando idioma: {e}")

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
