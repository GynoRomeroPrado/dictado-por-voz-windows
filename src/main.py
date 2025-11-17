"""
Main application entry point
Integrates all components: GUI, speech recognition, commands, and hotkeys
"""

import sys
import os

# Add src directory to path if running directly
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    __package__ = "src"

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal as pyqtSignal, Slot as pyqtSlot

# Handle both relative and absolute imports
try:
    from .gui.main_window import MainWindow
    from .core.speech_recognizer import SpeechRecognizer
    from .core.command_processor import CommandProcessor
    from .core.hotkey_manager import HotkeyManager
    from .utils.config import config
except ImportError:
    from gui.main_window import MainWindow
    from core.speech_recognizer import SpeechRecognizer
    from core.command_processor import CommandProcessor
    from core.hotkey_manager import HotkeyManager
    from utils.config import config


class VoiceDictationApp(QObject):
    """Main application controller"""

    def __init__(self):
        """Initialize the application"""
        super().__init__()

        # Components
        self.window = None
        self.recognizer = None
        self.command_processor = None
        self.hotkey_manager = None

        # State
        self.is_running = False

    def initialize(self):
        """Initialize all components"""
        print("Initializing Voice Dictation App...")

        # Initialize GUI
        self.window = MainWindow()

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

        print("Application initialized successfully")

    def connect_signals(self):
        """Connect GUI signals to handlers"""
        self.window.toggle_dictation_signal.connect(self.toggle_dictation)
        self.window.stop_dictation_signal.connect(self.stop_dictation)
        self.window.language_changed_signal.connect(self.change_language)
        self.window.clear_buffer_signal.connect(self.clear_buffer)

    def register_hotkeys(self):
        """Register global hotkeys"""
        try:
            self.hotkey_manager.register_default_hotkeys(
                toggle_callback=self.toggle_dictation,
                stop_callback=self.stop_dictation,
                settings_callback=self.open_settings
            )
            print("Hotkeys registered successfully")
        except Exception as e:
            print(f"Error registering hotkeys: {e}")

    def run(self):
        """Run the application"""
        self.is_running = True

        # Show window
        if config.get('ui.show_main_window', True):
            if not config.get('ui.start_minimized', False):
                self.window.show()
            else:
                self.window.hide()
        else:
            self.window.show()

        return app.exec_()

    @pyqtSlot()
    def toggle_dictation(self):
        """Toggle dictation on/off"""
        if self.recognizer.is_listening:
            self.stop_dictation()
        else:
            self.start_dictation()

    @pyqtSlot()
    def start_dictation(self):
        """Start voice dictation"""
        try:
            print("Starting dictation...")
            self.recognizer.start_listening()
            self.window.set_listening_state(True)
            self.window.show_notification("Dictado iniciado - Comienza a hablar")

            # Play beep if enabled
            if config.get('audio.beep_on_start', True):
                self.play_beep()

        except Exception as e:
            print(f"Error starting dictation: {e}")
            self.window.show_notification(f"Error al iniciar dictado: {e}")

    @pyqtSlot()
    def stop_dictation(self):
        """Stop voice dictation"""
        try:
            print("Stopping dictation...")
            self.recognizer.stop_listening()
            self.window.set_listening_state(False)
            self.window.show_notification("Dictado detenido")

            # Play beep if enabled
            if config.get('audio.beep_on_stop', True):
                self.play_beep()

        except Exception as e:
            print(f"Error stopping dictation: {e}")

    @pyqtSlot(str)
    def change_language(self, language_code: str):
        """
        Change recognition language

        Args:
            language_code: Language code (e.g., 'es-ES')
        """
        try:
            print(f"Changing language to: {language_code}")
            self.recognizer.set_language(language_code)
            self.window.show_notification(f"Idioma cambiado a: {language_code}")
        except Exception as e:
            print(f"Error changing language: {e}")

    @pyqtSlot()
    def clear_buffer(self):
        """Clear text buffer"""
        self.command_processor.clear_buffer()
        print("Buffer cleared")

    @pyqtSlot()
    def open_settings(self):
        """Open settings dialog"""
        self.window.on_open_settings()

    def on_text_recognized(self, text: str):
        """
        Callback for recognized text

        Args:
            text: Recognized text from speech
        """
        print(f"Text recognized: {text}")

        # Process text through command processor
        processed_text, is_action = self.command_processor.process_text(text)

        if is_action:
            # Action command executed, no text to insert
            print("Action command executed")
            return

        if processed_text:
            # Add to buffer
            self.command_processor.add_to_buffer(processed_text)

            # Update GUI preview
            self.window.append_text(processed_text)

            # Insert text into active application
            success = self.command_processor.insert_text(processed_text)

            if not success:
                print("Failed to insert text")
                self.window.show_notification("Error al insertar texto")

    def play_beep(self):
        """Play a beep sound"""
        try:
            import winsound
            winsound.Beep(1000, 100)  # 1000 Hz for 100 ms
        except Exception as e:
            print(f"Error playing beep: {e}")

    def cleanup(self):
        """Cleanup resources before exit"""
        print("Cleaning up...")

        # Stop dictation
        if self.recognizer and self.recognizer.is_listening:
            self.recognizer.stop_listening()

        # Unregister hotkeys
        if self.hotkey_manager:
            self.hotkey_manager.unregister_all()

        print("Cleanup complete")


def main():
    """Main entry point"""
    global app

    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("Dictado por Voz")
    app.setOrganizationName("Gyno Romero Prado")

    # Create and initialize main app
    voice_app = VoiceDictationApp()
    voice_app.initialize()

    # Run application
    exit_code = voice_app.run()

    # Cleanup
    voice_app.cleanup()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
