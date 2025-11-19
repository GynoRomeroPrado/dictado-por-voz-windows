"""
Aplicación simplificada de dictado por voz
Solo icono en bandeja + hotkey global + escritura directa donde está el cursor
"""

import sys
import os

# Add src directory to path if running directly
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    __package__ = "src"

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, Slot
import keyboard
import time

# Handle both relative and absolute imports
try:
    from .gui.tray_icon import TrayIcon
    from .gui.settings_dialog import SettingsDialog
    from .gui.quick_settings import QuickSettingsDialog
    from .gui.recording_overlay import RecordingOverlay, MinimalRecordingIndicator
    from .core.speech_recognizer import SpeechRecognizer
    from .core.command_processor import CommandProcessor
    from .core.hotkey_manager import HotkeyManager
    from .utils.config import config
except ImportError:
    from gui.tray_icon import TrayIcon
    from gui.settings_dialog import SettingsDialog
    from gui.quick_settings import QuickSettingsDialog
    from gui.recording_overlay import RecordingOverlay, MinimalRecordingIndicator
    from core.speech_recognizer import SpeechRecognizer
    from core.command_processor import CommandProcessor
    from core.hotkey_manager import HotkeyManager
    from utils.config import config


class SimpleDictationApp(QObject):
    """Aplicación minimalista de dictado por voz"""

    def __init__(self):
        """Initialize the application"""
        super().__init__()

        # Components
        self.tray_icon = None
        self.recognizer = None
        self.command_processor = None
        self.hotkey_manager = None
        self.settings_dialog = None
        self.quick_settings_dialog = None
        self.recording_overlay = None  # Ventana flotante moderna

        # State
        self.is_running = False

    def initialize(self):
        """Initialize all components"""
        print("Iniciando Dictado por Voz...")

        # Initialize tray icon (no main window)
        self.tray_icon = TrayIcon()

        # Initialize recording overlay (ventana flotante moderna)
        use_minimal = config.get('ui', 'minimal_indicator', fallback='false') == 'true'
        if use_minimal:
            self.recording_overlay = MinimalRecordingIndicator()
        else:
            self.recording_overlay = RecordingOverlay(theme='dark')

        # Initialize command processor
        self.command_processor = CommandProcessor()

        # Initialize speech recognizer with callback
        self.recognizer = SpeechRecognizer(callback=self.on_text_recognized)

        # Initialize hotkey manager
        self.hotkey_manager = HotkeyManager()

        # Connect signals
        self.connect_signals()

        # Register hotkeys
        self.register_hotkeys()

        print("✓ Aplicación iniciada correctamente")
        print(f"✓ Presiona {config.get('hotkeys.toggle_dictation', 'Ctrl+Shift+Space')} para iniciar dictado")

    def connect_signals(self):
        """Connect tray icon signals to handlers"""
        self.tray_icon.toggle_dictation_signal.connect(self.toggle_dictation)
        self.tray_icon.open_settings_signal.connect(self.open_settings)
        self.tray_icon.open_quick_settings_signal.connect(self.open_quick_settings)
        self.tray_icon.quit_signal.connect(self.quit_application)

    def register_hotkeys(self):
        """Register global hotkeys"""
        try:
            self.hotkey_manager.register_default_hotkeys(
                toggle_callback=self.toggle_dictation,
                stop_callback=self.stop_dictation,
                settings_callback=self.open_settings
            )
            print("✓ Hotkeys registrados correctamente")
        except Exception as e:
            print(f"✗ Error registrando hotkeys: {e}")
            print("  Asegúrate de ejecutar como administrador en Windows")

    def run(self):
        """Run the application"""
        self.is_running = True
        return app.exec()

    @Slot()
    def toggle_dictation(self):
        """Toggle dictation on/off"""
        if self.recognizer.is_listening:
            self.stop_dictation()
        else:
            self.start_dictation()

    @Slot()
    def start_dictation(self):
        """Start voice dictation"""
        try:
            print("\n▶ Iniciando dictado...")
            self.recognizer.start_listening()
            self.tray_icon.set_listening_state(True)

            # Mostrar ventana flotante moderna
            hotkey = config.get('hotkeys', 'toggle_dictation', fallback='Ctrl+Shift+Space')
            if isinstance(self.recording_overlay, MinimalRecordingIndicator):
                self.recording_overlay.show_recording()
            else:
                self.recording_overlay.show_recording(hotkey)

            self.tray_icon.show_notification(
                "Dictado Iniciado",
                "Comienza a hablar. El texto se escribirá donde está el cursor."
            )

            # Play beep if enabled
            if config.get('audio.beep_on_start', True):
                self.play_beep()

            print("🎤 Escuchando... Habla ahora")
            print("   El texto se escribirá directamente donde está el cursor")

        except Exception as e:
            print(f"✗ Error al iniciar dictado: {e}")
            self.tray_icon.show_notification("Error", f"No se pudo iniciar: {e}")

    @Slot()
    def stop_dictation(self):
        """Stop voice dictation"""
        try:
            print("\n⏹ Deteniendo dictado...")
            self.recognizer.stop_listening()
            self.tray_icon.set_listening_state(False)

            # Ocultar ventana flotante
            if isinstance(self.recording_overlay, MinimalRecordingIndicator):
                self.recording_overlay.hide_recording()
            else:
                self.recording_overlay.hide_overlay()

            self.tray_icon.show_notification(
                "Dictado Detenido",
                "Dictado pausado"
            )

            # Play beep if enabled
            if config.get('audio.beep_on_stop', True):
                self.play_beep()

            print("⏸ Dictado detenido")

        except Exception as e:
            print(f"✗ Error al detener dictado: {e}")

    @Slot()
    def open_settings(self):
        """Open settings dialog"""
        if not self.settings_dialog:
            self.settings_dialog = SettingsDialog()

        self.settings_dialog.show()
        self.settings_dialog.activateWindow()

    @Slot()
    def open_quick_settings(self):
        """Open quick settings dialog"""
        if not self.quick_settings_dialog:
            self.quick_settings_dialog = QuickSettingsDialog()

        self.quick_settings_dialog.show()
        self.quick_settings_dialog.activateWindow()

    @Slot()
    def quit_application(self):
        """Quit the application"""
        print("\n👋 Cerrando aplicación...")
        self.cleanup()
        QApplication.quit()

    def on_text_recognized(self, text: str):
        """
        Callback for recognized text - Escribe DIRECTAMENTE donde está el cursor

        Args:
            text: Recognized text from speech
        """
        print(f"📝 Reconocido: {text}")

        # Mostrar estado de procesamiento en overlay
        if not isinstance(self.recording_overlay, MinimalRecordingIndicator):
            self.recording_overlay.show_processing()

        # Process text through command processor
        processed_text, is_action = self.command_processor.process_text(text)

        if is_action:
            # Action command executed
            print(f"⚡ Comando ejecutado: {text}")
            return

        if processed_text:
            # Write text DIRECTLY where cursor is using keyboard
            try:
                # Use keyboard.write() to type the text where the cursor is
                keyboard.write(processed_text)
                print(f"✓ Escrito: {processed_text}")

            except Exception as e:
                print(f"✗ Error escribiendo texto: {e}")

                # Mostrar error en overlay
                if not isinstance(self.recording_overlay, MinimalRecordingIndicator):
                    self.recording_overlay.show_error("Error al escribir")

                # Fallback: try using clipboard
                try:
                    import pyperclip
                    pyperclip.copy(processed_text)
                    keyboard.send('ctrl+v')
                    print(f"✓ Escrito (usando portapapeles): {processed_text}")
                except Exception as e2:
                    print(f"✗ Error con portapapeles también: {e2}")

    def play_beep(self):
        """Play a beep sound"""
        try:
            import winsound
            winsound.Beep(1000, 100)  # 1000 Hz for 100 ms
        except Exception:
            pass  # Silently fail if winsound not available

    def cleanup(self):
        """Cleanup resources before exit"""
        print("🧹 Limpiando recursos...")

        # Stop dictation
        if self.recognizer and self.recognizer.is_listening:
            self.recognizer.stop_listening()

        # Unregister hotkeys
        if self.hotkey_manager:
            self.hotkey_manager.unregister_all()

        # Hide recording overlay
        if self.recording_overlay:
            if isinstance(self.recording_overlay, MinimalRecordingIndicator):
                self.recording_overlay.hide_recording()
            else:
                self.recording_overlay.hide_overlay()

        # Hide tray icon
        if self.tray_icon:
            self.tray_icon.hide()

        print("✓ Limpieza completada")


def main():
    """Main entry point"""
    global app

    print("""
╔════════════════════════════════════════════════════╗
║                                                    ║
║         🎤 DICTADO POR VOZ - WINDOWS 🎤           ║
║                                                    ║
║  Dictado universal para cualquier aplicación      ║
║                                                    ║
╚════════════════════════════════════════════════════╝
""")

    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("Dictado por Voz")
    app.setOrganizationName("Gyno Romero Prado")

    # Prevent app from quitting when last window closes
    # (we don't have a main window, just tray icon)
    app.setQuitOnLastWindowClosed(False)

    # Create and initialize main app
    voice_app = SimpleDictationApp()
    voice_app.initialize()

    print("\n" + "="*50)
    print("✓ Aplicación en ejecución")
    print("✓ Icono visible en la bandeja del sistema")
    print(f"✓ Presiona {config.get('hotkeys.toggle_dictation', 'Ctrl+Shift+Space')} para empezar a dictar")
    print("="*50 + "\n")

    # Run application
    exit_code = voice_app.run()

    # Cleanup
    voice_app.cleanup()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
