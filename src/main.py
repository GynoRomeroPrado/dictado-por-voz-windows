import sys
import threading
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, Slot
import keyboard

from core.engine import VoiceEngine
from core.keyboard_util import KeyboardInjector
from ui.window import ModernMainWindow

class AppController(QObject):
    log_signal = Signal(str)
    status_signal = Signal(bool)

    def __init__(self):
        super().__init__()
        
        # UI
        self.window = ModernMainWindow()
        self.window.toggle_requested.connect(self.toggle_dictation)
        self.window.close_requested.connect(self.cleanup)

        # Engine
        self.engine = VoiceEngine(
            on_text_recognized=self.on_text_recognized,
            on_status_change=self.on_status_update
        )
        
        # Conectar señales de hilos a UI
        self.log_signal.connect(self.window.log_message)
        self.status_signal.connect(self.window.update_status)

        # Global Hotkey (F2)
        # Usamos keyboard.add_hotkey que corre en su propio thread de fondo
        keyboard.add_hotkey('F2', self.toggle_dictation)

        self.window.show()
        self.log_signal.emit("Sistema iniciado. Presiona 'Iniciar' o F2.")

    @Slot()
    def toggle_dictation(self):
        # Esta función puede ser llamada desde UI (Main Thread) o Hotkey (Background Thread)
        # La lógica de engine es thread-safe
        if self.engine.listening:
            self.engine.stop_listening()
            # Actualizamos UI via señales
            self.status_signal.emit(False)
            self.log_signal.emit("Pausado.")
        else:
            self.engine.start_listening()
            self.status_signal.emit(True)
            self.log_signal.emit("Iniciando motor de voz...")

    def on_text_recognized(self, text):
        if text:
            self.log_signal.emit(f"Reconocido: {text}")
            # Inyectar texto (desde el thread del engine)
            KeyboardInjector.type_text(text)

    def on_status_update(self, status_text):
        self.log_signal.emit(f"Estado: {status_text}")

    def cleanup(self):
        self.engine.running = False
        keyboard.unhook_all()
        self.window.force_close()

def main():
    # Single Instance Logic
    # try:
    #     import win32event
    #     import win32api
    #     import winerror
    #     mutex_name = "Global\\DictadoPorVozWhisperMX"
    #     mutex = win32event.CreateMutex(None, False, mutex_name)
    #     if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    #         print("Instancia ya existe (Check deshabilitado temporalmente para debug).")
    #         # import ctypes
    #         # ctypes.windll.user32.MessageBoxW(0, "La aplicación ya está en ejecución (revisa la bandeja del sistema).", "Dictado por Voz", 0x40 | 0x1)
    #         # return
            
    # except ImportError:
    #     print("Advertencia: pywin32 no instalado, no se puede verificar instancia única.")

    # Identificador para Icono en Barra de Tareas
    try:
        import ctypes
        myappid = 'whisper.dictado.porvoz.mx.v2' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        pass

    app = QApplication(sys.argv)
    
    # Prevenir cierre automático si la ventana se oculta
    app.setQuitOnLastWindowClosed(False)
    
    controller = AppController()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
