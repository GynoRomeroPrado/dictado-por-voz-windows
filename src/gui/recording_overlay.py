"""
Ventana flotante moderna y minimalista para mostrar el estado de grabación
"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Property, QPoint
from PySide6.QtGui import QPainter, QColor, QPen

try:
    from .modern_styles import get_recording_overlay_style, COLORS
except ImportError:
    from modern_styles import get_recording_overlay_style, COLORS


class PulsingDot(QLabel):
    """Punto que pulsa para indicar grabación activa"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(12, 12)
        self._opacity = 1.0

        # Animación de pulso
        self.animation = QPropertyAnimation(self, b"opacity")
        self.animation.setDuration(1000)  # 1 segundo
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.3)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.animation.setLoopCount(-1)  # Infinito
        self.animation.start()

    def get_opacity(self):
        return self._opacity

    def set_opacity(self, value):
        self._opacity = value
        self.update()

    opacity = Property(float, get_opacity, set_opacity)

    def paintEvent(self, event):
        """Dibuja el punto con la opacidad actual"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Color rojo con opacidad variable
        color = QColor(239, 68, 68)  # danger red
        color.setAlphaF(self._opacity)

        painter.setBrush(color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, 12, 12)


class RecordingOverlay(QDialog):
    """
    Ventana flotante pequeña y moderna que muestra el estado de grabación
    """

    def __init__(self, parent=None, theme='dark'):
        super().__init__(parent)

        self.theme = theme
        self.is_recording = False

        # Configuración de ventana
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(False)

        # UI
        self.setup_ui()
        self.apply_styles()

        # Tamaño fijo pequeño
        self.setFixedSize(220, 70)

        # Posición inicial (esquina superior derecha)
        self.position_window()

        # Timer para ocultar automáticamente después de inactividad
        self.hide_timer = QTimer()
        self.hide_timer.timeout.connect(self.hide)
        self.hide_timer.setSingleShot(True)

    def setup_ui(self):
        """Configura la interfaz"""
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)
        self.setLayout(layout)

        # Layout horizontal para el punto y el texto
        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)

        # Punto pulsante
        self.pulsing_dot = PulsingDot()
        top_layout.addWidget(self.pulsing_dot)

        # Label de estado
        self.status_label = QLabel("Escuchando...")
        self.status_label.setObjectName("status")
        top_layout.addWidget(self.status_label)
        top_layout.addStretch()

        layout.addLayout(top_layout)

        # Subtítulo
        self.subtitle_label = QLabel("Presiona Ctrl+Shift+Space para detener")
        self.subtitle_label.setObjectName("subtitle")
        layout.addWidget(self.subtitle_label)

    def apply_styles(self):
        """Aplica los estilos modernos"""
        self.setStyleSheet(get_recording_overlay_style(self.theme))

    def position_window(self):
        """Posiciona la ventana en la esquina superior derecha"""
        from PySide6.QtGui import QGuiApplication

        screen = QGuiApplication.primaryScreen().geometry()
        x = screen.width() - self.width() - 20
        y = 20
        self.move(x, y)

    def show_recording(self, hotkey="Ctrl+Shift+Space"):
        """Muestra la ventana indicando que está grabando"""
        self.is_recording = True
        self.status_label.setText("Escuchando...")
        self.subtitle_label.setText(f"Presiona {hotkey} para detener")
        self.pulsing_dot.animation.start()
        self.show()
        self.raise_()
        self.activateWindow()

    def show_processing(self):
        """Muestra que está procesando"""
        self.status_label.setText("Procesando...")
        self.subtitle_label.setText("Escribiendo texto...")
        self.pulsing_dot.animation.stop()
        self.pulsing_dot.set_opacity(1.0)

        # Ocultar después de 2 segundos
        self.hide_timer.start(2000)

    def show_error(self, message="Error al reconocer"):
        """Muestra un mensaje de error"""
        self.status_label.setText(message)
        self.subtitle_label.setText("Intenta de nuevo")
        self.pulsing_dot.animation.stop()
        self.pulsing_dot.set_opacity(1.0)

        # Ocultar después de 3 segundos
        self.hide_timer.start(3000)

    def hide_overlay(self):
        """Oculta la ventana"""
        self.is_recording = False
        self.pulsing_dot.animation.stop()
        self.hide()

    def set_theme(self, theme):
        """Cambia el tema (dark/light)"""
        self.theme = theme
        self.apply_styles()

    # Permitir mover la ventana arrastrándola
    def mousePressEvent(self, event):
        """Detecta cuando se hace clic en la ventana"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Permite mover la ventana"""
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()


class MinimalRecordingIndicator(QDialog):
    """
    Indicador SUPER minimalista - solo un punto rojo flotante
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Ventana sin marco, siempre encima
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(False)

        # Tamaño mínimo
        self.setFixedSize(40, 40)

        # Posición
        self.position_indicator()

        # Animación de pulso
        self._opacity = 1.0
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.4)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.animation.setLoopCount(-1)

    def position_indicator(self):
        """Posiciona en la esquina superior derecha"""
        from PySide6.QtGui import QGuiApplication

        screen = QGuiApplication.primaryScreen().geometry()
        x = screen.width() - 60
        y = 20
        self.move(x, y)

    def paintEvent(self, event):
        """Dibuja el círculo rojo"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Círculo rojo
        painter.setBrush(QColor(239, 68, 68))
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        painter.drawEllipse(5, 5, 30, 30)

    def show_recording(self):
        """Muestra el indicador"""
        self.show()
        self.animation.start()

    def hide_recording(self):
        """Oculta el indicador"""
        self.animation.stop()
        self.hide()

    def mousePressEvent(self, event):
        """Detecta clics para mover"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        """Permite mover el indicador"""
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
