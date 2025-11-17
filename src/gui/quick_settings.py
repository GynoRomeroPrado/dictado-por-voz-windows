"""
Diálogo de configuración rápida accesible desde la bandeja del sistema
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QComboBox, QCheckBox, QPushButton, QLineEdit,
    QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt, Signal

try:
    from ..utils.config import config
    from ..utils.auto_start import AutoStart
except ImportError:
    from utils.config import config
    from utils.auto_start import AutoStart


class QuickSettingsDialog(QDialog):
    """Diálogo de configuración rápida"""

    # Signal emitido cuando cambia la configuración
    settings_changed = Signal()

    def __init__(self, parent=None):
        """Initialize quick settings dialog"""
        super().__init__(parent)

        self.setWindowTitle("⚙ Configuración Rápida - Dictado por Voz")
        self.setModal(False)
        self.setMinimumWidth(400)

        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # === IDIOMA ===
        lang_group = QGroupBox("🌍 Idioma de Reconocimiento")
        lang_layout = QFormLayout()

        self.language_combo = QComboBox()
        self.populate_languages()
        lang_layout.addRow("Idioma:", self.language_combo)

        lang_group.setLayout(lang_layout)
        layout.addWidget(lang_group)

        # === ATAJOS DE TECLADO ===
        hotkey_group = QGroupBox("⌨️ Atajos de Teclado")
        hotkey_layout = QFormLayout()

        self.hotkey_edit = QLineEdit()
        self.hotkey_edit.setPlaceholderText("ctrl+shift+space")
        hotkey_layout.addRow("Iniciar/Detener:", self.hotkey_edit)

        hint_label = QLabel("Ejemplos: ctrl+shift+space, alt+d, ctrl+alt+v")
        hint_label.setStyleSheet("color: gray; font-size: 10px;")
        hotkey_layout.addRow(hint_label)

        hotkey_group.setLayout(hotkey_layout)
        layout.addWidget(hotkey_group)

        # === AUTO-INICIO ===
        startup_group = QGroupBox("🚀 Inicio Automático")
        startup_layout = QVBoxLayout()

        self.autostart_check = QCheckBox("Iniciar con Windows")
        self.autostart_check.toggled.connect(self.on_autostart_toggled)
        startup_layout.addWidget(self.autostart_check)

        startup_group.setLayout(startup_layout)
        layout.addWidget(startup_group)

        # === NOTIFICACIONES ===
        notif_group = QGroupBox("🔔 Notificaciones")
        notif_layout = QVBoxLayout()

        self.notifications_check = QCheckBox("Mostrar notificaciones del sistema")
        notif_layout.addWidget(self.notifications_check)

        self.beep_start_check = QCheckBox("Beep al iniciar dictado")
        notif_layout.addWidget(self.beep_start_check)

        self.beep_stop_check = QCheckBox("Beep al detener dictado")
        notif_layout.addWidget(self.beep_stop_check)

        notif_group.setLayout(notif_layout)
        layout.addWidget(notif_group)

        # === BOTONES ===
        button_layout = QHBoxLayout()

        self.save_button = QPushButton("💾 Guardar")
        self.save_button.clicked.connect(self.save_settings)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        # Info footer
        info_label = QLabel("Los cambios se aplicarán al reiniciar la aplicación")
        info_label.setStyleSheet("color: gray; font-size: 10px; padding: 5px;")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)

    def populate_languages(self):
        """Populate language combo box"""
        languages = {
            'es-ES': '🇪🇸 Español (España)',
            'es-MX': '🇲🇽 Español (México)',
            'en-US': '🇺🇸 English (US)',
            'en-GB': '🇬🇧 English (UK)',
            'fr-FR': '🇫🇷 Français',
            'de-DE': '🇩🇪 Deutsch',
            'it-IT': '🇮🇹 Italiano',
            'pt-BR': '🇧🇷 Português (Brasil)',
            'pt-PT': '🇵🇹 Português (Portugal)',
        }

        for code, name in languages.items():
            self.language_combo.addItem(name, code)

    def load_settings(self):
        """Load current settings"""
        # Language
        current_lang = config.get('language', 'es-ES')
        index = self.language_combo.findData(current_lang)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)

        # Hotkey
        hotkey = config.get('hotkeys.toggle_dictation', 'ctrl+shift+space')
        self.hotkey_edit.setText(hotkey)

        # Auto-start
        self.autostart_check.setChecked(AutoStart.is_enabled())

        # Notifications
        self.notifications_check.setChecked(
            config.get('ui.show_notifications', True)
        )
        self.beep_start_check.setChecked(
            config.get('audio.beep_on_start', True)
        )
        self.beep_stop_check.setChecked(
            config.get('audio.beep_on_stop', True)
        )

    def save_settings(self):
        """Save settings"""
        try:
            # Language
            language_code = self.language_combo.currentData()
            config.set('language', language_code)

            # Hotkey
            hotkey = self.hotkey_edit.text().strip()
            if hotkey:
                config.set('hotkeys.toggle_dictation', hotkey)

            # Notifications
            config.set('ui.show_notifications', self.notifications_check.isChecked())
            config.set('audio.beep_on_start', self.beep_start_check.isChecked())
            config.set('audio.beep_on_stop', self.beep_stop_check.isChecked())

            # Emit signal
            self.settings_changed.emit()

            # Success message
            QMessageBox.information(
                self,
                "✓ Configuración Guardada",
                "La configuración se ha guardado correctamente.\n\n"
                "Reinicia la aplicación para aplicar todos los cambios."
            )

            self.accept()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error guardando la configuración:\n{e}"
            )

    def on_autostart_toggled(self, checked):
        """Handle auto-start toggle"""
        try:
            if checked:
                success = AutoStart.enable()
                if not success:
                    self.autostart_check.setChecked(False)
                    QMessageBox.warning(
                        self,
                        "Error",
                        "No se pudo habilitar el auto-inicio.\n"
                        "Ejecuta la aplicación como Administrador."
                    )
            else:
                AutoStart.disable()

        except Exception as e:
            self.autostart_check.setChecked(AutoStart.is_enabled())
            QMessageBox.critical(
                self,
                "Error",
                f"Error al cambiar auto-inicio:\n{e}"
            )
