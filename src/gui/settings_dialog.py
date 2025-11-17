"""
Settings dialog module
Configuration interface for the application
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
    QWidget, QLabel, QLineEdit, QPushButton, QCheckBox,
    QComboBox, QSpinBox, QDoubleSpinBox, QGroupBox,
    QFormLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from ..utils.config import config


class SettingsDialog(QDialog):
    """Settings configuration dialog"""

    def __init__(self, parent=None):
        """
        Initialize settings dialog

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        self.setWindowTitle("Configuración")
        self.setGeometry(150, 150, 600, 500)
        self.setModal(True)

        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Create tabs
        self.create_general_tab()
        self.create_recognition_tab()
        self.create_hotkeys_tab()
        self.create_output_tab()

        # Buttons
        button_layout = QHBoxLayout()

        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

    def create_general_tab(self):
        """Create general settings tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        # UI Settings
        ui_group = QGroupBox("Interfaz de Usuario")
        ui_layout = QFormLayout()

        self.show_window_check = QCheckBox("Mostrar ventana principal al iniciar")
        ui_layout.addRow(self.show_window_check)

        self.minimize_tray_check = QCheckBox("Minimizar a la bandeja del sistema")
        ui_layout.addRow(self.minimize_tray_check)

        self.start_minimized_check = QCheckBox("Iniciar minimizado")
        ui_layout.addRow(self.start_minimized_check)

        self.always_on_top_check = QCheckBox("Ventana siempre visible")
        ui_layout.addRow(self.always_on_top_check)

        self.show_notifications_check = QCheckBox("Mostrar notificaciones")
        ui_layout.addRow(self.show_notifications_check)

        ui_group.setLayout(ui_layout)
        layout.addWidget(ui_group)

        # Audio Feedback
        audio_group = QGroupBox("Retroalimentación de Audio")
        audio_layout = QFormLayout()

        self.feedback_enabled_check = QCheckBox("Habilitar retroalimentación de audio")
        audio_layout.addRow(self.feedback_enabled_check)

        self.beep_start_check = QCheckBox("Beep al iniciar dictado")
        audio_layout.addRow(self.beep_start_check)

        self.beep_stop_check = QCheckBox("Beep al detener dictado")
        audio_layout.addRow(self.beep_stop_check)

        audio_group.setLayout(audio_layout)
        layout.addWidget(audio_group)

        layout.addStretch()
        self.tabs.addTab(tab, "General")

    def create_recognition_tab(self):
        """Create recognition settings tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        # Recognition Engine
        engine_group = QGroupBox("Motor de Reconocimiento")
        engine_layout = QFormLayout()

        self.engine_combo = QComboBox()
        self.engine_combo.addItem("Google Speech Recognition", "google")
        self.engine_combo.addItem("Windows Speech Recognition", "windows")
        self.engine_combo.addItem("Sphinx (Offline)", "sphinx")
        engine_layout.addRow("Motor:", self.engine_combo)

        engine_group.setLayout(engine_layout)
        layout.addWidget(engine_group)

        # Recognition Parameters
        params_group = QGroupBox("Parámetros de Reconocimiento")
        params_layout = QFormLayout()

        self.confidence_spin = QDoubleSpinBox()
        self.confidence_spin.setRange(0.0, 1.0)
        self.confidence_spin.setSingleStep(0.1)
        self.confidence_spin.setDecimals(1)
        params_layout.addRow("Confianza mínima:", self.confidence_spin)

        self.energy_spin = QSpinBox()
        self.energy_spin.setRange(300, 8000)
        self.energy_spin.setSingleStep(100)
        params_layout.addRow("Umbral de energía:", self.energy_spin)

        self.dynamic_energy_check = QCheckBox("Ajuste dinámico de energía")
        params_layout.addRow(self.dynamic_energy_check)

        self.pause_spin = QDoubleSpinBox()
        self.pause_spin.setRange(0.1, 3.0)
        self.pause_spin.setSingleStep(0.1)
        self.pause_spin.setDecimals(1)
        params_layout.addRow("Umbral de pausa (s):", self.pause_spin)

        params_group.setLayout(params_layout)
        layout.addWidget(params_group)

        layout.addStretch()
        self.tabs.addTab(tab, "Reconocimiento")

    def create_hotkeys_tab(self):
        """Create hotkeys settings tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        hotkeys_group = QGroupBox("Atajos de Teclado Globales")
        hotkeys_layout = QFormLayout()

        info_label = QLabel(
            "Usa combinaciones como: ctrl+shift+space, alt+d, etc.\n"
            "Separa teclas con '+'"
        )
        info_label.setStyleSheet("color: gray; font-size: 9px;")
        hotkeys_layout.addRow(info_label)

        self.toggle_hotkey_edit = QLineEdit()
        hotkeys_layout.addRow("Iniciar/Detener Dictado:", self.toggle_hotkey_edit)

        self.stop_hotkey_edit = QLineEdit()
        hotkeys_layout.addRow("Detener Dictado:", self.stop_hotkey_edit)

        self.settings_hotkey_edit = QLineEdit()
        hotkeys_layout.addRow("Abrir Configuración:", self.settings_hotkey_edit)

        test_button = QPushButton("Probar Atajo")
        test_button.clicked.connect(self.test_hotkey)
        hotkeys_layout.addRow(test_button)

        hotkeys_group.setLayout(hotkeys_layout)
        layout.addWidget(hotkeys_group)

        layout.addStretch()
        self.tabs.addTab(tab, "Atajos de Teclado")

    def create_output_tab(self):
        """Create output settings tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        output_group = QGroupBox("Configuración de Salida")
        output_layout = QFormLayout()

        self.auto_insert_check = QCheckBox("Insertar automáticamente en aplicación activa")
        output_layout.addRow(self.auto_insert_check)

        self.use_clipboard_check = QCheckBox("Usar portapapeles para insertar")
        output_layout.addRow(self.use_clipboard_check)

        self.auto_copy_check = QCheckBox("Copiar automáticamente al portapapeles")
        output_layout.addRow(self.auto_copy_check)

        self.paste_delay_spin = QDoubleSpinBox()
        self.paste_delay_spin.setRange(0.0, 2.0)
        self.paste_delay_spin.setSingleStep(0.1)
        self.paste_delay_spin.setDecimals(1)
        output_layout.addRow("Retraso al pegar (s):", self.paste_delay_spin)

        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        # Advanced Settings
        advanced_group = QGroupBox("Configuración Avanzada")
        advanced_layout = QFormLayout()

        self.auto_punctuation_check = QCheckBox("Puntuación automática")
        advanced_layout.addRow(self.auto_punctuation_check)

        self.auto_capitalization_check = QCheckBox("Capitalización automática")
        advanced_layout.addRow(self.auto_capitalization_check)

        self.enable_custom_commands_check = QCheckBox("Habilitar comandos personalizados")
        advanced_layout.addRow(self.enable_custom_commands_check)

        self.save_transcriptions_check = QCheckBox("Guardar transcripciones")
        advanced_layout.addRow(self.save_transcriptions_check)

        advanced_group.setLayout(advanced_layout)
        layout.addWidget(advanced_group)

        layout.addStretch()
        self.tabs.addTab(tab, "Salida")

    def load_settings(self):
        """Load current settings from config"""
        # General - UI
        self.show_window_check.setChecked(config.get('ui.show_main_window', True))
        self.minimize_tray_check.setChecked(config.get('ui.minimize_to_tray', True))
        self.start_minimized_check.setChecked(config.get('ui.start_minimized', False))
        self.always_on_top_check.setChecked(config.get('ui.always_on_top', False))
        self.show_notifications_check.setChecked(config.get('ui.show_notifications', True))

        # General - Audio
        self.feedback_enabled_check.setChecked(config.get('audio.feedback_enabled', True))
        self.beep_start_check.setChecked(config.get('audio.beep_on_start', True))
        self.beep_stop_check.setChecked(config.get('audio.beep_on_stop', True))

        # Recognition
        engine = config.get('recognition.engine', 'google')
        index = self.engine_combo.findData(engine)
        if index >= 0:
            self.engine_combo.setCurrentIndex(index)

        self.confidence_spin.setValue(config.get('recognition.confidence_threshold', 0.7))
        self.energy_spin.setValue(config.get('recognition.energy_threshold', 4000))
        self.dynamic_energy_check.setChecked(config.get('recognition.dynamic_energy', True))
        self.pause_spin.setValue(config.get('recognition.pause_threshold', 0.8))

        # Hotkeys
        self.toggle_hotkey_edit.setText(config.get('hotkeys.toggle_dictation', 'ctrl+shift+space'))
        self.stop_hotkey_edit.setText(config.get('hotkeys.stop_dictation', 'ctrl+shift+s'))
        self.settings_hotkey_edit.setText(config.get('hotkeys.open_settings', 'ctrl+shift+o'))

        # Output
        self.auto_insert_check.setChecked(config.get('output.auto_insert', True))
        self.use_clipboard_check.setChecked(config.get('output.use_clipboard', False))
        self.auto_copy_check.setChecked(config.get('output.auto_copy', True))
        self.paste_delay_spin.setValue(config.get('output.paste_delay', 0.1))

        # Advanced
        self.auto_punctuation_check.setChecked(config.get('advanced.auto_punctuation', True))
        self.auto_capitalization_check.setChecked(config.get('advanced.auto_capitalization', True))
        self.enable_custom_commands_check.setChecked(config.get('advanced.enable_custom_commands', True))
        self.save_transcriptions_check.setChecked(config.get('advanced.save_transcriptions', False))

    def save_settings(self):
        """Save settings to config"""
        # General - UI
        config.set('ui.show_main_window', self.show_window_check.isChecked())
        config.set('ui.minimize_to_tray', self.minimize_tray_check.isChecked())
        config.set('ui.start_minimized', self.start_minimized_check.isChecked())
        config.set('ui.always_on_top', self.always_on_top_check.isChecked())
        config.set('ui.show_notifications', self.show_notifications_check.isChecked())

        # General - Audio
        config.set('audio.feedback_enabled', self.feedback_enabled_check.isChecked())
        config.set('audio.beep_on_start', self.beep_start_check.isChecked())
        config.set('audio.beep_on_stop', self.beep_stop_check.isChecked())

        # Recognition
        config.set('recognition.engine', self.engine_combo.currentData())
        config.set('recognition.confidence_threshold', self.confidence_spin.value())
        config.set('recognition.energy_threshold', self.energy_spin.value())
        config.set('recognition.dynamic_energy', self.dynamic_energy_check.isChecked())
        config.set('recognition.pause_threshold', self.pause_spin.value())

        # Hotkeys
        config.set('hotkeys.toggle_dictation', self.toggle_hotkey_edit.text())
        config.set('hotkeys.stop_dictation', self.stop_hotkey_edit.text())
        config.set('hotkeys.open_settings', self.settings_hotkey_edit.text())

        # Output
        config.set('output.auto_insert', self.auto_insert_check.isChecked())
        config.set('output.use_clipboard', self.use_clipboard_check.isChecked())
        config.set('output.auto_copy', self.auto_copy_check.isChecked())
        config.set('output.paste_delay', self.paste_delay_spin.value())

        # Advanced
        config.set('advanced.auto_punctuation', self.auto_punctuation_check.isChecked())
        config.set('advanced.auto_capitalization', self.auto_capitalization_check.isChecked())
        config.set('advanced.enable_custom_commands', self.enable_custom_commands_check.isChecked())
        config.set('advanced.save_transcriptions', self.save_transcriptions_check.isChecked())

        # Show confirmation
        QMessageBox.information(
            self,
            "Configuración Guardada",
            "La configuración se ha guardado correctamente.\n"
            "Algunos cambios pueden requerir reiniciar la aplicación."
        )

        self.accept()

    def test_hotkey(self):
        """Test hotkey validity"""
        from ..core.hotkey_manager import HotkeyManager

        hotkey = self.toggle_hotkey_edit.text()
        if HotkeyManager.test_hotkey(hotkey):
            QMessageBox.information(
                self,
                "Atajo Válido",
                f"El atajo '{hotkey}' es válido."
            )
        else:
            QMessageBox.warning(
                self,
                "Atajo Inválido",
                f"El atajo '{hotkey}' no es válido.\n"
                "Usa el formato: ctrl+shift+space, alt+d, etc."
            )
