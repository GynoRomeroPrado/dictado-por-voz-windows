import sys
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QPushButton, QPlainTextEdit, 
                             QHBoxLayout, QSystemTrayIcon, QMenu, QFrame, QStyle, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, Signal, Slot, QSize, QTimer
from PySide6.QtGui import QIcon, QAction, QFont, QColor, QPalette, QLinearGradient, QBrush, QPixmap

class ModernMainWindow(QMainWindow):
    # Definir señales
    toggle_requested = Signal()
    close_requested = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dictado por Voz - Whisper MX")
        self.resize(500, 400)
        
        # Setup UI standard
        self.setup_ui()
        self.setup_menu()
        self.setup_tray()
        self.apply_styles()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Header con info clara
        self.status_label = QLabel("Estado: Esperando modelo...")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ccc;")
        layout.addWidget(self.status_label)

        # Botón Grande y Claro
        self.toggle_btn = QPushButton("Iniciar Dictado (F2)")
        self.toggle_btn.setMinimumHeight(50)
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.emit_toggle)
        self.toggle_btn.setEnabled(False) # Deshabilitado hasta que cargue
        layout.addWidget(self.toggle_btn)

        # Muestra el texto
        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)
        self.console.setPlaceholderText("El texto reconocido aparecerá aquí...")
        layout.addWidget(self.console)

    def setup_menu(self):
        menu_bar = self.menuBar()
        
        # Menu Archivo
        file_menu = menu_bar.addMenu("Archivo")
        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.force_close)
        file_menu.addAction(exit_action)
        
        # Menu Opciones (Placeholder para mostrar que existen)
        opt_menu = menu_bar.addMenu("Opciones")
        
        model_action = QAction("Modelo: Small (Default)", self)
        model_action.setEnabled(False)
        opt_menu.addAction(model_action)
        
        mic_action = QAction("Micrófono: Default System", self)
        mic_action.setEnabled(False)
        opt_menu.addAction(mic_action)

    def setup_tray(self):
        from PySide6.QtWidgets import QStyle
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        
        tray_menu = QMenu()
        show_action = QAction("Abrir Ventana", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        quit_action = QAction("Salir Totalmente", self)
        quit_action.triggered.connect(self.force_close)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.on_tray_activated)

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage("Dictado Segundo Plano", "La app sigue corriendo aquí.", QSystemTrayIcon.Information, 1500)

    def force_close(self):
        self.tray_icon.hide()
        sys.exit(0)

    def emit_toggle(self):
        self.toggle_requested.emit()

    def update_status(self, is_active):
        if is_active:
            self.status_label.setText("Estado: ESCUCHANDO")
            self.status_label.setStyleSheet("color: #0f0; font-weight: bold; font-size: 14px;")
            self.toggle_btn.setText("Detener Dictado (F2)")
        else:
            self.status_label.setText("Estado: En espera (F2 para dictar)")
            self.status_label.setStyleSheet("color: #ccc; font-weight: bold; font-size: 14px;")
            self.toggle_btn.setText("Iniciar Dictado (F2)")

    def log_message(self, msg):
        self.console.appendPlainText(msg)
        # Lógica para habilitar botón cuando acaba la carga
        if "Modelo listo" in msg:
            self.toggle_btn.setEnabled(True)
            self.status_label.setText("Modelo Cargado. Listo.")

    def apply_styles(self):
        # Tema Oscuro Funcional (estilo VS Code)
        self.setStyleSheet("""
            QMainWindow { background-color: #2b2b2b; color: #fff; }
            QLabel { color: #fff; }
            QPlainTextEdit { background-color: #1e1e1e; color: #d4d4d4; font-family: Consolas; border: 1px solid #3c3c3c; }
            QPushButton { background-color: #0e639c; color: #fff; border: none; padding: 10px; font-size: 14px; }
            QPushButton:hover { background-color: #1177bb; }
            QPushButton:disabled { background-color: #3a3a3a; color: #888; }
            QMenuBar { background-color: #333; color: #fff; }
            QMenuBar::item:selected { background-color: #555; }
            QMenu { background-color: #252526; color: #fff; }
            QMenu::item:selected { background-color: #094771; }
        """)
