"""
FloatingWidget - Botón flotante y overlay de texto para dictado
Permite controlar dictado desde cualquier lugar y previsualizar texto
"""

import logging
import math
from typing import Optional

from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout,
    QApplication, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal, QTimer, QRect
from PySide6.QtGui import (
    QFont, QColor, QPainter, QPainterPath, QBrush, QPen
)

logger = logging.getLogger(__name__)


class FloatingMicButton(QWidget):
    """
    Botón flotante de micrófono.
    Verde = inactivo, Rojo = activo con animación de latido
    """
    
    clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._is_active = False
        self._size = 55
        self._pulse_value = 0.0
        
        # Ventana sin bordes, siempre visible
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(self._size, self._size)
        
        # Posicionar
        self._position_top_right()
        
        # Timer para animación
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_pulse)
        self._timer.setInterval(50)
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        logger.info("Botón flotante creado")
    
    def _position_top_right(self):
        screen = QApplication.primaryScreen()
        if screen:
            geo = screen.availableGeometry()
            self.move(geo.right() - self._size - 20, geo.top() + 20)
    
    def set_active(self, active: bool):
        """Cambia estado activo/inactivo"""
        logger.info(f"FloatingMicButton.set_active({active})")
        self._is_active = active
        
        if active:
            self._pulse_value = 0.0
            self._timer.start()
        else:
            self._timer.stop()
            self._pulse_value = 0.0
        
        self.update()
    
    def _on_pulse(self):
        """Animación de pulso"""
        self._pulse_value += 0.2
        if self._pulse_value > 2 * math.pi:
            self._pulse_value = 0.0
        self.update()
    
    def paintEvent(self, event):
        """Dibuja el botón"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Tamaño y offset
        margin = 3
        circle_size = self._size - margin * 2
        
        # Escala para animación (solo cuando activo)
        if self._is_active:
            scale = 1.0 + 0.08 * math.sin(self._pulse_value)
            circle_size = int(circle_size * scale)
        
        offset = (self._size - circle_size) // 2
        
        # Colores
        if self._is_active:
            # Rojo pulsante
            brightness = int(200 + 55 * math.sin(self._pulse_value))
            bg = QColor(brightness, 50, 60)
            border = QColor(180, 40, 50)
        else:
            # Verde estático
            bg = QColor(40, 180, 70)
            border = QColor(30, 150, 60)
        
        # Dibujar círculo
        painter.setBrush(QBrush(bg))
        painter.setPen(QPen(border, 2))
        painter.drawEllipse(offset, offset, circle_size, circle_size)
        
        # Dibujar micrófono centrado
        painter.setPen(QPen(Qt.GlobalColor.white, 2))
        painter.setBrush(QBrush(Qt.GlobalColor.white))
        
        cx = self._size // 2
        cy = self._size // 2
        
        # Cuerpo del mic
        mic_w, mic_h = 10, 14
        mic_x = cx - mic_w // 2
        mic_y = cy - mic_h // 2 - 3
        
        path = QPainterPath()
        path.addRoundedRect(mic_x, mic_y, mic_w, mic_h, 4, 4)
        painter.drawPath(path)
        
        # Arco
        painter.setBrush(Qt.BrushStyle.NoBrush)
        arc_w = mic_w + 6
        arc_rect = QRect(cx - arc_w // 2, mic_y + mic_h - 3, arc_w, 8)
        painter.drawArc(arc_rect, 0, -180 * 16)
        
        # Base
        painter.drawLine(cx, cy + 8, cx, cy + 12)
        painter.drawLine(cx - 5, cy + 12, cx + 5, cy + 12)
    
    def mousePressEvent(self, event):
        """Inicia arrastre o click"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start_pos = event.globalPosition().toPoint()
            self._widget_start_pos = self.pos()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Arrastra el botón"""
        if event.buttons() == Qt.MouseButton.LeftButton:
            if hasattr(self, '_drag_start_pos'):
                delta = event.globalPosition().toPoint() - self._drag_start_pos
                new_pos = self._widget_start_pos + delta
                self.move(new_pos)
                self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """Detecta si fue clic o arrastre"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            
            if hasattr(self, '_drag_start_pos'):
                # Si se movió poco, es un clic
                delta = event.globalPosition().toPoint() - self._drag_start_pos
                if abs(delta.x()) < 5 and abs(delta.y()) < 5:
                    logger.info("Botón flotante clickeado!")
                    self.clicked.emit()
                else:
                    logger.debug(f"Botón movido a posición: {self.pos()}")
                
                # Limpiar
                delattr(self, '_drag_start_pos')
                delattr(self, '_widget_start_pos')
            
            event.accept()



class TextOverlay(QWidget):
    """Overlay para mostrar texto dictado"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setFont(QFont("Segoe UI", 30, QFont.Weight.Bold))
        self.label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 240);
                background-color: rgba(40, 40, 40, 190);
                border-radius: 18px;
                padding: 20px 30px;
            }
        """)
        layout.addWidget(self.label)
        
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.hide)
        
        self.hide()
    
    def show_text(self, text: str):
        if not text.strip():
            return
        
        self.label.setText(text)
        self.adjustSize()
        
        # Centrar en pantalla
        screen = QApplication.primaryScreen()
        if screen:
            geo = screen.availableGeometry()
            x = geo.center().x() - self.width() // 2
            y = geo.top() + int(geo.height() * 0.18)
            self.move(x, y)
        
        self.setWindowOpacity(1.0)
        self.show()
        
        self._timer.stop()
        self._timer.start(3500)
    
    def clear(self):
        self.label.setText("")
        self.hide()


class FloatingWidgetManager:
    """Administra botón flotante y overlay"""
    
    def __init__(self):
        self.mic_button = FloatingMicButton()
        self.text_overlay = TextOverlay()
        self.on_toggle_dictation = None
        
        self.mic_button.clicked.connect(self._on_click)
        logger.info("FloatingWidgetManager inicializado")
    
    def _on_click(self):
        logger.info("FloatingWidgetManager._on_click llamado")
        if self.on_toggle_dictation:
            self.on_toggle_dictation()
    
    def set_listening_state(self, listening: bool):
        logger.info(f"FloatingWidgetManager.set_listening_state({listening})")
        self.mic_button.set_active(listening)
        if listening:
            self.text_overlay.clear()
    
    def show_recognized_text(self, text: str):
        self.text_overlay.show_text(text)
    
    def show(self):
        self.mic_button.show()
    
    def hide(self):
        self.mic_button.hide()
        self.text_overlay.hide()
