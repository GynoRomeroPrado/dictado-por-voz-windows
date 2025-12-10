"""
SettingsDialog - Diálogo de configuración
Permite ajustar idioma, hotkeys, modelo y otras opciones
"""

import logging
from typing import Optional

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLabel, QComboBox, QLineEdit,
    QCheckBox, QTabWidget, QWidget, QGroupBox,
    QSpinBox, QSlider, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from ..utils.config import config

logger = logging.getLogger(__name__)


class HotkeyEdit(QLineEdit):
    """Widget personalizado para capturar combinaciones de teclas"""
    
    hotkey_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setPlaceholderText("Presiona una combinación de teclas...")
        self._capturing = False
        self._modifiers = []
        self._key = ""
    
    def mousePressEvent(self, event):
        """Activa el modo de captura al hacer clic"""
        self._capturing = True
        self._modifiers = []
        self._key = ""
        self.setText("Esperando teclas...")
        self.setStyleSheet("background-color: #3d5afe;")
        super().mousePressEvent(event)
    
    def keyPressEvent(self, event):
        """Captura la combinación de teclas"""
        if not self._capturing:
            return
        
        # Capturar modificadores
        modifiers = event.modifiers()
        mod_list = []
        
        if modifiers & Qt.KeyboardModifier.ControlModifier:
            mod_list.append("ctrl")
        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            mod_list.append("shift")
        if modifiers & Qt.KeyboardModifier.AltModifier:
            mod_list.append("alt")
        
        # Capturar tecla principal
        key = event.key()
        key_name = ""
        
        # Ignorar teclas modificadoras solas
        if key not in (Qt.Key.Key_Control, Qt.Key.Key_Shift, Qt.Key.Key_Alt, Qt.Key.Key_Meta):
            if Qt.Key.Key_A <= key <= Qt.Key.Key_Z:
                key_name = chr(key).lower()
            elif Qt.Key.Key_0 <= key <= Qt.Key.Key_9:
                key_name = chr(key)
            elif key == Qt.Key.Key_Space:
                key_name = "space"
            elif key == Qt.Key.Key_Escape:
                # Cancelar captura
                self._capturing = False
                self.setText(self._current_hotkey if hasattr(self, '_current_hotkey') else "")
                self.setStyleSheet("")
                return
            else:
                # Otras teclas
                key_name = event.text().lower() if event.text() else ""
        
        if mod_list and key_name:
            combo = "+".join(mod_list + [key_name])
            self._capturing = False
            self.setText(combo)
            self.setStyleSheet("")
            self._current_hotkey = combo
            self.hotkey_changed.emit(combo)
    
    def set_hotkey(self, hotkey: str) -> None:
        """Establece el hotkey actual"""
        self._current_hotkey = hotkey
        self.setText(hotkey)


class SettingsDialog(QDialog):
    """
    Diálogo para configurar la aplicación.
    Organizado en pestañas: General, Reconocimiento, Hotkeys, Avanzado.
    """
    
    settings_changed = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Configuración - Dictado por Voz")
        self.setMinimumSize(500, 450)
        self.resize(550, 500)
        
        self._setup_ui()
        self._load_settings()
        
        logger.info("Diálogo de configuración inicializado")
    
    def _setup_ui(self) -> None:
        """Configura la interfaz del diálogo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Pestañas
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # === Pestaña General ===
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        
        # Idioma
        lang_group = QGroupBox("Idioma")
        lang_layout = QFormLayout(lang_group)
        
        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "Español (Perú) - es-PE",
            "Español (México) - es-MX",
            "Español (Argentina) - es-AR",
            "Español (Colombia) - es-CO",
            "Español (Chile) - es-CL",
            "Español (España) - es-ES",
            "English (US) - en-US",
            "English (UK) - en-GB",
            "Português (Brasil) - pt-BR",
            "Français - fr-FR",
            "Deutsch - de-DE",
            "Italiano - it-IT"
        ])
        lang_layout.addRow("Idioma de reconocimiento:", self.language_combo)
        general_layout.addWidget(lang_group)
        
        # UI
        ui_group = QGroupBox("Interfaz")
        ui_layout = QFormLayout(ui_group)
        
        self.minimize_to_tray_check = QCheckBox("Minimizar a la bandeja al cerrar")
        ui_layout.addRow(self.minimize_to_tray_check)
        
        self.always_on_top_check = QCheckBox("Mantener ventana siempre visible")
        ui_layout.addRow(self.always_on_top_check)
        
        self.show_notifications_check = QCheckBox("Mostrar notificaciones")
        ui_layout.addRow(self.show_notifications_check)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Automático", "Oscuro", "Claro"])
        ui_layout.addRow("Tema:", self.theme_combo)
        
        general_layout.addWidget(ui_group)
        general_layout.addStretch()
        
        self.tabs.addTab(general_tab, "General")
        
        # === Pestaña Reconocimiento ===
        recognition_tab = QWidget()
        recognition_layout = QVBoxLayout(recognition_tab)
        
        # Modelo
        model_group = QGroupBox("Motor de Reconocimiento")
        model_layout = QFormLayout(model_group)
        
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "tiny - Más rápido, menor precisión",
            "base - Equilibrado",
            "small - Buena precisión (recomendado)",
            "medium - Alta precisión (lento)",
            "large-v3 - Máxima precisión (muy lento)",
            "large-v3-turbo - Buena velocidad + precisión"
        ])
        model_layout.addRow("Modelo Whisper:", self.model_combo)
        recognition_layout.addWidget(model_group)
        
        # Audio
        audio_group = QGroupBox("Audio")
        audio_layout = QFormLayout(audio_group)
        
        self.energy_threshold_spin = QSpinBox()
        self.energy_threshold_spin.setRange(100, 5000)
        self.energy_threshold_spin.setSingleStep(50)
        audio_layout.addRow("Umbral de energía:", self.energy_threshold_spin)
        
        self.pause_threshold_spin = QSpinBox()
        self.pause_threshold_spin.setRange(1, 30)
        self.pause_threshold_spin.setSuffix(" décimas de segundo")
        audio_layout.addRow("Pausa entre frases:", self.pause_threshold_spin)
        
        self.dynamic_energy_check = QCheckBox("Ajuste dinámico de umbral")
        audio_layout.addRow(self.dynamic_energy_check)
        
        recognition_layout.addWidget(audio_group)
        recognition_layout.addStretch()
        
        self.tabs.addTab(recognition_tab, "Reconocimiento")
        
        # === Pestaña Hotkeys ===
        hotkeys_tab = QWidget()
        hotkeys_layout = QVBoxLayout(hotkeys_tab)
        
        hotkeys_group = QGroupBox("Atajos de Teclado")
        hotkeys_form = QFormLayout(hotkeys_group)
        
        self.toggle_hotkey_edit = HotkeyEdit()
        hotkeys_form.addRow("Activar/desactivar dictado:", self.toggle_hotkey_edit)
        
        self.stop_hotkey_edit = HotkeyEdit()
        hotkeys_form.addRow("Detener dictado:", self.stop_hotkey_edit)
        
        self.settings_hotkey_edit = HotkeyEdit()
        hotkeys_form.addRow("Abrir configuración:", self.settings_hotkey_edit)
        
        hotkeys_layout.addWidget(hotkeys_group)
        
        hotkeys_info = QLabel(
            "💡 Haz clic en un campo y presiona la combinación de teclas deseada.\n"
            "Presiona Escape para cancelar."
        )
        hotkeys_info.setStyleSheet("color: #888888; font-size: 11px;")
        hotkeys_layout.addWidget(hotkeys_info)
        hotkeys_layout.addStretch()
        
        self.tabs.addTab(hotkeys_tab, "Hotkeys")
        
        # === Pestaña Avanzado ===
        advanced_tab = QWidget()
        advanced_layout = QVBoxLayout(advanced_tab)
        
        formatting_group = QGroupBox("Formato")
        formatting_layout = QFormLayout(formatting_group)
        
        self.auto_capitalization_check = QCheckBox("Capitalización automática")
        formatting_layout.addRow(self.auto_capitalization_check)
        
        self.auto_punctuation_check = QCheckBox("Puntuación automática")
        formatting_layout.addRow(self.auto_punctuation_check)
        
        self.custom_commands_check = QCheckBox("Habilitar comandos personalizados")
        formatting_layout.addRow(self.custom_commands_check)
        
        advanced_layout.addWidget(formatting_group)
        
        output_group = QGroupBox("Salida")
        output_layout = QFormLayout(output_group)
        
        self.auto_insert_check = QCheckBox("Insertar texto automáticamente")
        output_layout.addRow(self.auto_insert_check)
        
        self.use_clipboard_check = QCheckBox("Usar portapapeles (Ctrl+V)")
        output_layout.addRow(self.use_clipboard_check)
        
        advanced_layout.addWidget(output_group)
        advanced_layout.addStretch()
        
        self.tabs.addTab(advanced_tab, "Avanzado")
        
        # === Botones ===
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("Guardar")
        self.save_button.setDefault(True)
        self.save_button.clicked.connect(self._save_settings)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
    
    def _load_settings(self) -> None:
        """Carga la configuración actual en los widgets"""
        # Idioma
        language = config.get('language', 'es-MX')
        for i in range(self.language_combo.count()):
            if language in self.language_combo.itemText(i):
                self.language_combo.setCurrentIndex(i)
                break
        
        # UI
        self.minimize_to_tray_check.setChecked(config.get('ui.minimize_to_tray', True))
        self.always_on_top_check.setChecked(config.get('ui.always_on_top', False))
        self.show_notifications_check.setChecked(config.get('ui.show_notifications', True))
        
        theme = config.get('ui.theme', 'auto')
        theme_map = {'auto': 0, 'dark': 1, 'light': 2}
        self.theme_combo.setCurrentIndex(theme_map.get(theme, 0))
        
        # Modelo
        model = config.get('recognition.model', 'base')
        model_names = ['tiny', 'base', 'small', 'medium', 'large-v3', 'large-v3-turbo']
        if model in model_names:
            self.model_combo.setCurrentIndex(model_names.index(model))
        
        # Audio
        self.energy_threshold_spin.setValue(config.get('recognition.energy_threshold', 600))
        pause = config.get('recognition.pause_threshold', 0.8)
        self.pause_threshold_spin.setValue(int(pause * 10))
        self.dynamic_energy_check.setChecked(config.get('recognition.dynamic_energy', True))
        
        # Hotkeys
        self.toggle_hotkey_edit.set_hotkey(config.get('hotkeys.toggle_dictation', 'ctrl+shift+space'))
        self.stop_hotkey_edit.set_hotkey(config.get('hotkeys.stop_dictation', 'ctrl+shift+s'))
        self.settings_hotkey_edit.set_hotkey(config.get('hotkeys.open_settings', 'ctrl+shift+o'))
        
        # Avanzado
        self.auto_capitalization_check.setChecked(config.get('advanced.auto_capitalization', True))
        self.auto_punctuation_check.setChecked(config.get('advanced.auto_punctuation', True))
        self.custom_commands_check.setChecked(config.get('advanced.enable_custom_commands', True))
        self.auto_insert_check.setChecked(config.get('output.auto_insert', True))
        self.use_clipboard_check.setChecked(config.get('output.use_clipboard', False))
    
    def _save_settings(self) -> None:
        """Guarda la configuración"""
        # Idioma
        lang_text = self.language_combo.currentText()
        lang_code = lang_text.split(' - ')[-1] if ' - ' in lang_text else 'es-MX'
        config.set('language', lang_code)
        
        # UI
        config.set('ui.minimize_to_tray', self.minimize_to_tray_check.isChecked())
        config.set('ui.always_on_top', self.always_on_top_check.isChecked())
        config.set('ui.show_notifications', self.show_notifications_check.isChecked())
        
        theme_map = {0: 'auto', 1: 'dark', 2: 'light'}
        config.set('ui.theme', theme_map.get(self.theme_combo.currentIndex(), 'auto'))
        
        # Modelo
        model_names = ['tiny', 'base', 'small', 'medium', 'large-v3', 'large-v3-turbo']
        config.set('recognition.model', model_names[self.model_combo.currentIndex()])
        
        # Audio
        config.set('recognition.energy_threshold', self.energy_threshold_spin.value())
        config.set('recognition.pause_threshold', self.pause_threshold_spin.value() / 10.0)
        config.set('recognition.dynamic_energy', self.dynamic_energy_check.isChecked())
        
        # Hotkeys
        config.set('hotkeys.toggle_dictation', self.toggle_hotkey_edit.text())
        config.set('hotkeys.stop_dictation', self.stop_hotkey_edit.text())
        config.set('hotkeys.open_settings', self.settings_hotkey_edit.text())
        
        # Avanzado
        config.set('advanced.auto_capitalization', self.auto_capitalization_check.isChecked())
        config.set('advanced.auto_punctuation', self.auto_punctuation_check.isChecked())
        config.set('advanced.enable_custom_commands', self.custom_commands_check.isChecked())
        config.set('output.auto_insert', self.auto_insert_check.isChecked())
        config.set('output.use_clipboard', self.use_clipboard_check.isChecked())
        
        # Guardar y emitir señal
        config.save_config()
        self.settings_changed.emit()
        
        logger.info("Configuración guardada")
        self.accept()
