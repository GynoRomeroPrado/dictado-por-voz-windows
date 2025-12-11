"""
SystemTrayIcon - Icono en la bandeja del sistema
Permite controlar la aplicación desde la bandeja de Windows
"""

import logging
from typing import Optional, Callable

from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QAction
from PySide6.QtCore import Signal, QObject

from ..utils.config import config

logger = logging.getLogger(__name__)


class SystemTrayIcon(QSystemTrayIcon):
    """
    Icono de la bandeja del sistema.
    Muestra estado y proporciona acceso rápido a las funciones principales.
    """
    
    # Señales
    toggle_requested = Signal()
    show_window_requested = Signal()
    settings_requested = Signal()
    exit_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._is_listening = False
        
        # Intentar cargar icono personalizado
        from pathlib import Path
        icon_path = Path(__file__).parent.parent / "assets" / "app_icon.ico"
        
        if icon_path.exists():
            # Usar icono personalizado
            from PySide6.QtGui import QIcon
            self._idle_icon = QIcon(str(icon_path))
            self._listening_icon = QIcon(str(icon_path))  # Mismo icono por ahora
            self._error_icon = self._create_circle_icon(QColor(244, 67, 54))
            logger.info(f"Icono personalizado cargado para tray: {icon_path}")
        else:
            # Fallback: crear iconos generados
            self._create_icons()
            logger.warning("Icono personalizado no encontrado, usando generado")
        
        self.setIcon(self._idle_icon)
        
        # Crear menú contextual
        self._setup_menu()
        
        # Conectar señales
        self.activated.connect(self._on_activated)
        
        # Mostrar
        self.setToolTip("Dictado por Voz - Listo")
        self.show()
        
        logger.info("Icono de bandeja inicializado")
    
    def _create_icons(self) -> None:
        """Crea los iconos para diferentes estados"""
        # Icono en estado inactivo (gris)
        self._idle_icon = self._create_circle_icon(QColor(100, 100, 100))
        
        # Icono en estado activo/escuchando (verde)
        self._listening_icon = self._create_circle_icon(QColor(76, 175, 80))
        
        # Icono de error (rojo)
        self._error_icon = self._create_circle_icon(QColor(244, 67, 54))
    
    def _create_circle_icon(self, color: QColor) -> QIcon:
        """
        Crea un icono circular con el color especificado.
        
        Args:
            color: Color del círculo
            
        Returns:
            QIcon con el círculo
        """
        size = 64
        pixmap = QPixmap(size, size)
        pixmap.fill(QColor(0, 0, 0, 0))  # Transparente
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dibujar círculo con micrófono estilizado
        painter.setBrush(color)
        painter.setPen(QColor(255, 255, 255, 50))
        margin = 4
        painter.drawEllipse(margin, margin, size - 2*margin, size - 2*margin)
        
        # Dibujar símbolo de micrófono simplificado
        painter.setPen(QColor(255, 255, 255))
        painter.setBrush(QColor(255, 255, 255))
        
        # Cuerpo del micrófono
        mic_width = 12
        mic_height = 20
        mic_x = (size - mic_width) // 2
        mic_y = size // 4
        painter.drawRoundedRect(mic_x, mic_y, mic_width, mic_height, 4, 4)
        
        # Arco inferior
        arc_y = mic_y + mic_height - 2
        painter.drawArc(mic_x - 4, arc_y, mic_width + 8, 16, 0, -180 * 16)
        
        # Línea base
        line_x = size // 2
        painter.drawLine(line_x, arc_y + 12, line_x, arc_y + 18)
        painter.drawLine(line_x - 6, arc_y + 18, line_x + 6, arc_y + 18)
        
        painter.end()
        
        return QIcon(pixmap)
    
    def _setup_menu(self) -> None:
        """Configura el menú contextual"""
        self.menu = QMenu()
        
        # Acción: Mostrar ventana
        self.show_action = QAction("Mostrar ventana", self)
        self.show_action.triggered.connect(self.show_window_requested.emit)
        self.menu.addAction(self.show_action)
        
        self.menu.addSeparator()
        
        # Acción: Toggle dictado
        self.toggle_action = QAction("🎤 Iniciar dictado", self)
        self.toggle_action.triggered.connect(self.toggle_requested.emit)
        self.menu.addAction(self.toggle_action)
        
        # Acción: Configuración
        self.settings_action = QAction("⚙️ Configuración", self)
        self.settings_action.triggered.connect(self.settings_requested.emit)
        self.menu.addAction(self.settings_action)
        
        self.menu.addSeparator()
        
        # Acción: Salir
        self.exit_action = QAction("❌ Salir", self)
        self.exit_action.triggered.connect(self.exit_requested.emit)
        self.menu.addAction(self.exit_action)
        
        self.setContextMenu(self.menu)
    
    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        """
        Maneja la activación del icono.
        
        Args:
            reason: Razón de activación (click, doble click, etc.)
        """
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            # Click izquierdo - toggle dictado
            self.toggle_requested.emit()
        elif reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            # Doble click - mostrar ventana
            self.show_window_requested.emit()
    
    def set_listening_state(self, is_listening: bool) -> None:
        """
        Actualiza el estado visual del icono.
        
        Args:
            is_listening: True si está escuchando
        """
        self._is_listening = is_listening
        
        if is_listening:
            self.setIcon(self._listening_icon)
            self.setToolTip("Dictado por Voz - Escuchando...")
            self.toggle_action.setText("⏹️ Detener dictado")
        else:
            self.setIcon(self._idle_icon)
            self.setToolTip("Dictado por Voz - Listo")
            self.toggle_action.setText("🎤 Iniciar dictado")
    
    def show_notification(self, title: str, message: str, 
                          icon: QSystemTrayIcon.MessageIcon = QSystemTrayIcon.MessageIcon.Information,
                          duration: int = 3000) -> None:
        """
        Muestra una notificación del sistema.
        
        Args:
            title: Título de la notificación
            message: Mensaje de la notificación
            icon: Tipo de icono
            duration: Duración en milisegundos
        """
        if config.get('ui.show_notifications', True):
            self.showMessage(title, message, icon, duration)
    
    def show_error(self, message: str) -> None:
        """
        Muestra el icono de error y una notificación.
        
        Args:
            message: Mensaje de error
        """
        self.setIcon(self._error_icon)
        self.show_notification(
            "Error - Dictado por Voz",
            message,
            QSystemTrayIcon.MessageIcon.Critical
        )
