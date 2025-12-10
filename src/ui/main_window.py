"""
MainWindow - Ventana principal de Dictado por Voz
Interfaz moderna con tema oscuro usando PySide6 y qdarktheme
"""

import logging
from typing import Optional

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QFrame, QProgressBar,
    QStatusBar, QMessageBox
)
from PySide6.QtCore import Qt, Slot, QTimer
from PySide6.QtGui import QFont, QIcon, QCloseEvent

from ..utils.config import config

logger = logging.getLogger(__name__)


class StatusIndicator(QFrame):
    """Widget indicador de estado visual (escuchando/detenido)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(20, 20)
        self._is_active = False
        self._update_style()
    
    def set_active(self, active: bool) -> None:
        """Establece el estado activo/inactivo"""
        self._is_active = active
        self._update_style()
    
    def _update_style(self) -> None:
        """Actualiza el estilo según el estado"""
        if self._is_active:
            self.setStyleSheet("""
                QFrame {
                    background-color: #4CAF50;
                    border-radius: 10px;
                    border: 2px solid #45a049;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background-color: #666666;
                    border-radius: 10px;
                    border: 2px solid #555555;
                }
            """)


class MainWindow(QMainWindow):
    """
    Ventana principal de la aplicación.
    Muestra el estado del dictado y el historial de texto reconocido.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Dictado por Voz")
        self.setMinimumSize(500, 400)
        self.resize(600, 500)
        
        # Estado
        self._is_listening = False
        
        # Callbacks (serán configurados externamente)
        self.on_toggle_dictation = None
        self.on_stop_dictation = None
        self.on_open_settings = None
        self.on_clear_history = None
        self.on_close_to_tray = None
        
        self._setup_ui()
        self._load_settings()
        
        logger.info("Ventana principal inicializada")
    
    def _setup_ui(self) -> None:
        """Configura la interfaz de usuario"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # === Sección de estado ===
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        status_layout = QHBoxLayout(status_frame)
        
        # Indicador visual
        self.status_indicator = StatusIndicator()
        status_layout.addWidget(self.status_indicator)
        
        # Texto de estado
        self.status_label = QLabel("Listo para dictar")
        self.status_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        status_layout.addWidget(self.status_label)
        
        status_layout.addStretch()
        
        # Hotkey info
        hotkey = config.get('hotkeys.toggle_dictation', 'Ctrl+Shift+Space')
        self.hotkey_label = QLabel(f"Presiona {hotkey}")
        self.hotkey_label.setStyleSheet("color: #888888;")
        status_layout.addWidget(self.hotkey_label)
        
        main_layout.addWidget(status_frame)
        
        # === Historial de texto ===
        history_label = QLabel("Historial de transcripción:")
        history_label.setFont(QFont("Segoe UI", 10))
        main_layout.addWidget(history_label)
        
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        self.history_text.setPlaceholderText("El texto reconocido aparecerá aquí...")
        self.history_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 10px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
            }
        """)
        main_layout.addWidget(self.history_text, 1)
        
        # === Botones ===
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Botón de dictado
        self.toggle_button = QPushButton("🎤 Iniciar Dictado")
        self.toggle_button.setFont(QFont("Segoe UI", 11))
        self.toggle_button.setMinimumHeight(45)
        self.toggle_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_button.clicked.connect(self._on_toggle_clicked)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        button_layout.addWidget(self.toggle_button, 2)
        
        # Botón limpiar
        self.clear_button = QPushButton("🗑️ Limpiar")
        self.clear_button.setMinimumHeight(45)
        self.clear_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_button.clicked.connect(self._on_clear_clicked)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 10px 15px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
            }
        """)
        button_layout.addWidget(self.clear_button)
        
        # Botón configuración
        self.settings_button = QPushButton("⚙️ Configuración")
        self.settings_button.setMinimumHeight(45)
        self.settings_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settings_button.clicked.connect(self._on_settings_clicked)
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 10px 15px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
            }
        """)
        button_layout.addWidget(self.settings_button)
        
        main_layout.addLayout(button_layout)
        
        # === Barra de estado ===
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Listo")
    
    def _load_settings(self) -> None:
        """Carga configuración de la ventana"""
        # Configurar siempre visible si está habilitado
        if config.get('ui.always_on_top', False):
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
    
    def _on_toggle_clicked(self) -> None:
        """Manejador del botón de toggle"""
        if self.on_toggle_dictation:
            self.on_toggle_dictation()
    
    def _on_clear_clicked(self) -> None:
        """Manejador del botón limpiar"""
        self.history_text.clear()
        if self.on_clear_history:
            self.on_clear_history()
    
    def _on_settings_clicked(self) -> None:
        """Manejador del botón de configuración"""
        if self.on_open_settings:
            self.on_open_settings()
    
    @Slot(bool)
    def set_listening_state(self, is_listening: bool) -> None:
        """
        Actualiza el estado visual de escucha.
        
        Args:
            is_listening: True si está escuchando
        """
        self._is_listening = is_listening
        self.status_indicator.set_active(is_listening)
        
        if is_listening:
            self.status_label.setText("🎤 Escuchando...")
            self.toggle_button.setText("⏹️ Detener Dictado")
            self.toggle_button.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
            """)
            self.statusBar.showMessage("Escuchando... Habla ahora")
        else:
            self.status_label.setText("Listo para dictar")
            self.toggle_button.setText("🎤 Iniciar Dictado")
            self.toggle_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            self.statusBar.showMessage("Listo")
    
    @Slot(str)
    def append_text(self, text: str) -> None:
        """
        Añade texto al historial.
        
        Args:
            text: Texto a añadir
        """
        if text:
            current = self.history_text.toPlainText()
            separator = " " if current and not current.endswith('\n') else ""
            self.history_text.setPlainText(current + separator + text)
            
            # Scroll al final
            scrollbar = self.history_text.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
    
    @Slot(str)
    def show_error(self, message: str) -> None:
        """
        Muestra un mensaje de error.
        
        Args:
            message: Mensaje de error
        """
        self.statusBar.showMessage(f"Error: {message}", 5000)
        logger.error(message)
    
    def closeEvent(self, event: QCloseEvent) -> None:
        """Maneja el evento de cierre de ventana"""
        if config.get('ui.minimize_to_tray', True):
            event.ignore()
            self.hide()
            if self.on_close_to_tray:
                self.on_close_to_tray()
        else:
            event.accept()
