"""
Main window GUI module
PyQt5 based interface for the voice dictation app
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QComboBox,
    QSystemTrayIcon, QMenu, QAction, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
import sys
from ..utils.config import config


class MainWindow(QMainWindow):
    """Main application window"""

    # Signals
    toggle_dictation_signal = pyqtSignal()
    stop_dictation_signal = pyqtSignal()
    language_changed_signal = pyqtSignal(str)
    clear_buffer_signal = pyqtSignal()

    def __init__(self):
        """Initialize main window"""
        super().__init__()

        self.is_listening = False
        self.setup_ui()
        self.setup_tray_icon()

        # Load settings
        self.load_settings()

    def setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("Dictado por Voz - Windows")
        self.setGeometry(100, 100, 600, 500)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Title
        title_label = QLabel("🎤 Dictado por Voz")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Status label
        self.status_label = QLabel("Estado: Detenido")
        self.status_label.setAlignment(Qt.AlignCenter)
        status_font = QFont()
        status_font.setPointSize(12)
        self.status_label.setFont(status_font)
        layout.addWidget(self.status_label)

        # Language selector
        lang_layout = QHBoxLayout()
        lang_label = QLabel("Idioma:")
        self.language_combo = QComboBox()
        self.populate_languages()
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.language_combo)
        lang_layout.addStretch()
        layout.addLayout(lang_layout)

        # Control buttons
        button_layout = QHBoxLayout()

        self.start_button = QPushButton("▶ Iniciar Dictado")
        self.start_button.setMinimumHeight(50)
        self.start_button.clicked.connect(self.on_toggle_dictation)
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("⏹ Detener")
        self.stop_button.setMinimumHeight(50)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.on_stop_dictation)
        button_layout.addWidget(self.stop_button)

        layout.addLayout(button_layout)

        # Text preview area
        preview_label = QLabel("Vista previa del texto:")
        layout.addWidget(preview_label)

        self.text_preview = QTextEdit()
        self.text_preview.setReadOnly(True)
        self.text_preview.setMaximumHeight(200)
        layout.addWidget(self.text_preview)

        # Action buttons
        action_layout = QHBoxLayout()

        self.clear_button = QPushButton("🗑 Limpiar")
        self.clear_button.clicked.connect(self.on_clear_buffer)
        action_layout.addWidget(self.clear_button)

        self.copy_button = QPushButton("📋 Copiar")
        self.copy_button.clicked.connect(self.on_copy_text)
        action_layout.addWidget(self.copy_button)

        self.settings_button = QPushButton("⚙ Configuración")
        self.settings_button.clicked.connect(self.on_open_settings)
        action_layout.addWidget(self.settings_button)

        layout.addLayout(action_layout)

        # Info label
        hotkey = config.get('hotkeys.toggle_dictation', 'Ctrl+Shift+Space')
        info_label = QLabel(f"Atajo de teclado: {hotkey}")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: gray; font-size: 10px;")
        layout.addWidget(info_label)

        # Instructions
        instructions = QLabel(
            "Instrucciones:\n"
            "1. Selecciona el idioma\n"
            "2. Haz clic en 'Iniciar Dictado' o usa el atajo de teclado\n"
            "3. Habla claramente en tu micrófono\n"
            "4. El texto se insertará automáticamente en la aplicación activa"
        )
        instructions.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
        layout.addWidget(instructions)

        layout.addStretch()

    def setup_tray_icon(self):
        """Setup system tray icon"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return

        # Create tray icon (using default icon for now)
        self.tray_icon = QSystemTrayIcon(self)
        # self.tray_icon.setIcon(QIcon('icon.png'))  # Add custom icon

        # Create tray menu
        tray_menu = QMenu()

        show_action = QAction("Mostrar", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)

        toggle_action = QAction("Iniciar/Detener Dictado", self)
        toggle_action.triggered.connect(self.on_toggle_dictation)
        tray_menu.addAction(toggle_action)

        tray_menu.addSeparator()

        quit_action = QAction("Salir", self)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        # Show tray icon
        if config.get('ui.minimize_to_tray', True):
            self.tray_icon.show()

    def populate_languages(self):
        """Populate language combo box"""
        languages = {
            'es-ES': 'Español (España)',
            'es-MX': 'Español (México)',
            'en-US': 'English (US)',
            'en-GB': 'English (UK)',
            'fr-FR': 'Français',
            'de-DE': 'Deutsch',
            'it-IT': 'Italiano',
            'pt-BR': 'Português (Brasil)',
            'pt-PT': 'Português (Portugal)',
        }

        current_lang = config.get('language', 'es-ES')

        for code, name in languages.items():
            self.language_combo.addItem(name, code)

        # Set current language
        index = self.language_combo.findData(current_lang)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)

    def load_settings(self):
        """Load settings from config"""
        # Window settings
        if config.get('ui.always_on_top', False):
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        if config.get('ui.start_minimized', False):
            self.hide()

    def on_toggle_dictation(self):
        """Toggle dictation on/off"""
        self.toggle_dictation_signal.emit()

    def on_stop_dictation(self):
        """Stop dictation"""
        self.stop_dictation_signal.emit()

    def on_language_changed(self, language_name):
        """Handle language change"""
        language_code = self.language_combo.currentData()
        if language_code:
            self.language_changed_signal.emit(language_code)

    def on_clear_buffer(self):
        """Clear text buffer"""
        self.text_preview.clear()
        self.clear_buffer_signal.emit()

    def on_copy_text(self):
        """Copy text to clipboard"""
        from ..utils.clipboard import ClipboardManager
        text = self.text_preview.toPlainText()
        if text:
            ClipboardManager.copy_to_clipboard(text)
            self.show_notification("Texto copiado al portapapeles", 2000)

    def on_open_settings(self):
        """Open settings dialog"""
        from .settings_dialog import SettingsDialog
        dialog = SettingsDialog(self)
        dialog.exec_()

    def on_tray_icon_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.show()
                self.activateWindow()

    def set_listening_state(self, is_listening: bool):
        """
        Update UI based on listening state

        Args:
            is_listening: True if currently listening
        """
        self.is_listening = is_listening

        if is_listening:
            self.status_label.setText("Estado: 🔴 Escuchando...")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            self.start_button.setText("⏸ Pausar Dictado")
            self.stop_button.setEnabled(True)
        else:
            self.status_label.setText("Estado: Detenido")
            self.status_label.setStyleSheet("color: gray;")
            self.start_button.setText("▶ Iniciar Dictado")
            self.stop_button.setEnabled(False)

    def append_text(self, text: str):
        """
        Append text to preview area

        Args:
            text: Text to append
        """
        self.text_preview.append(text)

    def show_notification(self, message: str, duration: int = 3000):
        """
        Show notification message

        Args:
            message: Message to show
            duration: Duration in milliseconds
        """
        if config.get('ui.show_notifications', True):
            if hasattr(self, 'tray_icon') and self.tray_icon.isVisible():
                self.tray_icon.showMessage(
                    "Dictado por Voz",
                    message,
                    QSystemTrayIcon.Information,
                    duration
                )

    def closeEvent(self, event):
        """Handle window close event"""
        if config.get('ui.minimize_to_tray', True):
            event.ignore()
            self.hide()
            self.show_notification("Aplicación minimizada a la bandeja del sistema")
        else:
            self.quit_application()

    def quit_application(self):
        """Quit the application"""
        reply = QMessageBox.question(
            self,
            'Confirmar salida',
            '¿Estás seguro de que quieres salir?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Emit stop signal
            self.stop_dictation_signal.emit()
            # Quit application
            from PyQt5.QtWidgets import QApplication
            QApplication.quit()
