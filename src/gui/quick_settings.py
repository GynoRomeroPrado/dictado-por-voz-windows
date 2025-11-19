"""
Diálogo de configuración rápida con diseño moderno y minimalista
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QCheckBox, QPushButton, QLineEdit, QWidget, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

try:
    from ..utils.config import config
    from ..utils.auto_start import AutoStart
    from .modern_styles import get_modern_stylesheet
except ImportError:
    from utils.config import config
    from utils.auto_start import AutoStart
    from modern_styles import get_modern_stylesheet


class ModernQuickSettings(QDialog):
    """
    Diálogo de configuración rápida con diseño moderno
    """

    settings_changed = Signal()

    def __init__(self, parent=None, theme='dark'):
        super().__init__(parent)

        self.theme = theme
        self.setWindowTitle("Configuración - Dictado por Voz")
        self.setModal(False)
        self.setFixedWidth(480)

        # Quitar marco de ventana por defecto
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.FramelessWindowHint
        )

        self.setup_ui()
        self.load_settings()
        self.apply_styles()

    def setup_ui(self):
        """Configura la interfaz moderna"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        # === HEADER ===
        header = self.create_header()
        main_layout.addWidget(header)

        # === CONTENT ===
        content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(24, 20, 24, 24)
        content_layout.setSpacing(20)
        content.setLayout(content_layout)

        # Idioma
        content_layout.addWidget(self.create_language_section())

        # Atajos
        content_layout.addWidget(self.create_hotkey_section())

        # Auto-inicio
        content_layout.addWidget(self.create_autostart_section())

        # Notificaciones
        content_layout.addWidget(self.create_notifications_section())

        content_layout.addStretch()

        main_layout.addWidget(content)

        # === FOOTER CON BOTONES ===
        footer = self.create_footer()
        main_layout.addWidget(footer)

    def create_header(self):
        """Crea el header moderno"""
        header = QFrame()
        header.setObjectName("header")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(24, 20, 24, 20)
        header.setLayout(header_layout)

        # Título
        title = QLabel("⚙ Configuración")
        title.setObjectName("title")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)

        header_layout.addWidget(title)
        header_layout.addStretch()

        # Botón cerrar
        close_btn = QPushButton("✕")
        close_btn.setObjectName("secondary")
        close_btn.setFixedSize(32, 32)
        close_btn.setToolTip("Cerrar")
        close_btn.clicked.connect(self.accept)

        header_layout.addWidget(close_btn)

        return header

    def create_language_section(self):
        """Sección de idioma"""
        section = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(8)
        section.setLayout(layout)

        # Título de sección
        label = QLabel("🌍 Idioma de reconocimiento")
        label_font = QFont()
        label_font.setPointSize(12)
        label_font.setBold(True)
        label.setFont(label_font)
        layout.addWidget(label)

        # Descripción
        desc = QLabel("Selecciona el idioma para el reconocimiento de voz")
        desc.setObjectName("subtitle")
        layout.addWidget(desc)

        # ComboBox
        self.language_combo = QComboBox()
        self.populate_languages()
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        layout.addWidget(self.language_combo)

        return section

    def create_hotkey_section(self):
        """Sección de atajos"""
        section = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(8)
        section.setLayout(layout)

        # Título
        label = QLabel("⌨️ Atajo de teclado")
        label_font = QFont()
        label_font.setPointSize(12)
        label_font.setBold(True)
        label.setFont(label_font)
        layout.addWidget(label)

        # Descripción
        desc = QLabel("Presiona esta combinación para iniciar/detener el dictado")
        desc.setObjectName("subtitle")
        layout.addWidget(desc)

        # Input
        self.hotkey_edit = QLineEdit()
        self.hotkey_edit.setPlaceholderText("ctrl+shift+space")
        self.hotkey_edit.textChanged.connect(self.on_hotkey_changed)
        layout.addWidget(self.hotkey_edit)

        # Hint
        hint = QLabel("💡 Ejemplos: ctrl+shift+space, alt+d, ctrl+alt+v")
        hint.setObjectName("subtitle")
        hint.setStyleSheet("font-size: 11px; padding: 4px 8px;")
        layout.addWidget(hint)

        return section

    def create_autostart_section(self):
        """Sección de auto-inicio"""
        section = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(8)
        section.setLayout(layout)

        # Título
        label = QLabel("🚀 Inicio automático")
        label_font = QFont()
        label_font.setPointSize(12)
        label_font.setBold(True)
        label.setFont(label_font)
        layout.addWidget(label)

        # Checkbox
        self.autostart_check = QCheckBox("Iniciar automáticamente con Windows")
        self.autostart_check.toggled.connect(self.on_autostart_toggled)
        layout.addWidget(self.autostart_check)

        return section

    def create_notifications_section(self):
        """Sección de notificaciones"""
        section = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(8)
        section.setLayout(layout)

        # Título
        label = QLabel("🔔 Notificaciones")
        label_font = QFont()
        label_font.setPointSize(12)
        label_font.setBold(True)
        label.setFont(label_font)
        layout.addWidget(label)

        # Checkboxes
        self.show_notifications_check = QCheckBox("Mostrar notificaciones")
        self.show_notifications_check.setChecked(
            config.get('notifications', 'show_notifications', fallback='true') == 'true'
        )
        self.show_notifications_check.toggled.connect(self.on_notifications_changed)
        layout.addWidget(self.show_notifications_check)

        self.play_beeps_check = QCheckBox("Reproducir sonidos")
        self.play_beeps_check.setChecked(
            config.get('notifications', 'play_beeps', fallback='true') == 'true'
        )
        self.play_beeps_check.toggled.connect(self.on_beeps_changed)
        layout.addWidget(self.play_beeps_check)

        return section

    def create_footer(self):
        """Crea el footer con botones"""
        footer = QFrame()
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(24, 16, 24, 16)
        footer.setLayout(footer_layout)

        # Botón de restaurar defaults
        restore_btn = QPushButton("Restaurar valores predeterminados")
        restore_btn.setObjectName("secondary")
        restore_btn.clicked.connect(self.restore_defaults)
        footer_layout.addWidget(restore_btn)

        footer_layout.addStretch()

        # Botón guardar
        save_btn = QPushButton("Guardar cambios")
        save_btn.clicked.connect(self.save_and_close)
        footer_layout.addWidget(save_btn)

        return footer

    def populate_languages(self):
        """Puebla el combobox de idiomas"""
        languages = {
            'Español (España)': 'es-ES',
            'English (US)': 'en-US',
            'English (UK)': 'en-GB',
            'Français': 'fr-FR',
            'Deutsch': 'de-DE',
            'Italiano': 'it-IT',
            'Português (Brasil)': 'pt-BR',
            'Português (Portugal)': 'pt-PT',
        }

        for display, code in languages.items():
            self.language_combo.addItem(display, code)

    def load_settings(self):
        """Carga la configuración actual"""
        # Idioma
        current_lang = config.get('speech', 'language', fallback='es-ES')
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == current_lang:
                self.language_combo.setCurrentIndex(i)
                break

        # Hotkey
        hotkey = config.get('hotkeys', 'toggle_dictation', fallback='ctrl+shift+space')
        self.hotkey_edit.setText(hotkey)

        # Auto-inicio
        self.autostart_check.setChecked(AutoStart.is_enabled())

    def apply_styles(self):
        """Aplica los estilos modernos"""
        self.setStyleSheet(get_modern_stylesheet(self.theme))

    def on_language_changed(self, text):
        """Cuando cambia el idioma"""
        lang_code = self.language_combo.currentData()
        if lang_code:
            config.set('speech', 'language', lang_code)
            config.save()

    def on_hotkey_changed(self, text):
        """Cuando cambia el hotkey"""
        if text:
            config.set('hotkeys', 'toggle_dictation', text)
            config.save()

    def on_autostart_toggled(self, checked):
        """Cuando cambia el auto-inicio"""
        try:
            if checked:
                AutoStart.enable()
            else:
                AutoStart.disable()
        except Exception as e:
            print(f"Error al cambiar auto-inicio: {e}")

    def on_notifications_changed(self, checked):
        """Cuando cambian las notificaciones"""
        config.set('notifications', 'show_notifications', str(checked).lower())
        config.save()

    def on_beeps_changed(self, checked):
        """Cuando cambian los beeps"""
        config.set('notifications', 'play_beeps', str(checked).lower())
        config.save()

    def restore_defaults(self):
        """Restaura los valores predeterminados"""
        # Idioma
        self.language_combo.setCurrentIndex(0)  # Español por defecto

        # Hotkey
        self.hotkey_edit.setText('ctrl+shift+space')

        # Auto-inicio
        self.autostart_check.setChecked(False)
        AutoStart.disable()

        # Notificaciones
        self.show_notifications_check.setChecked(True)
        self.play_beeps_check.setChecked(True)

        # Guardar
        config.set('speech', 'language', 'es-ES')
        config.set('hotkeys', 'toggle_dictation', 'ctrl+shift+space')
        config.set('notifications', 'show_notifications', 'true')
        config.set('notifications', 'play_beeps', 'true')
        config.save()

    def save_and_close(self):
        """Guarda y cierra el diálogo"""
        self.settings_changed.emit()
        self.accept()

    def set_theme(self, theme):
        """Cambia el tema"""
        self.theme = theme
        self.apply_styles()

    # Permitir mover la ventana
    def mousePressEvent(self, event):
        """Detecta clics para mover"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        """Permite mover la ventana"""
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)


# Mantener compatibilidad con el nombre anterior
QuickSettingsDialog = ModernQuickSettings
