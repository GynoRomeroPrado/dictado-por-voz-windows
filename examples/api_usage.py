"""
Ejemplos de uso de la API de Dictado por Voz

Este archivo muestra cómo usar los componentes del proyecto
programáticamente en tus propias aplicaciones.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Example 1: Using ConfigManager
def example_config_manager():
    """Ejemplo de uso del gestor de configuración"""
    from utils.config import ConfigManager

    # Create config manager
    config = ConfigManager()

    # Get settings
    language = config.get('language')
    print(f"Current language: {language}")

    # Set a setting
    config.set('language', 'en-US')
    print(f"Language changed to: {config.get('language')}")

    # Get nested setting
    engine = config.get('recognition.engine')
    print(f"Recognition engine: {engine}")

    # Add custom command
    new_command = {
        "id": "my_command",
        "enabled": True,
        "trigger": "my email",
        "action": "insert_text",
        "value": "example@email.com",
        "description": "Insert my email"
    }
    config.add_custom_command(new_command)
    print("Custom command added")


# Example 2: Using ClipboardManager (requires keyboard module)
def example_clipboard():
    """Ejemplo de uso del gestor de portapapeles"""
    try:
        from utils.clipboard import ClipboardManager

        clipboard = ClipboardManager()

        # Copy to clipboard
        clipboard.copy_to_clipboard("Hello from API!")
        print("Text copied to clipboard")

        # Get clipboard content
        content = clipboard.paste_from_clipboard()
        print(f"Clipboard content: {content}")

        # Insert text (requires keyboard module)
        # clipboard.insert_text("Inserted text")

        # Type text
        # clipboard.type_text("Typed text", delay=0.01)

    except ImportError:
        print("keyboard module not installed - some features unavailable")


# Example 3: Using SpeechRecognizer (requires speech_recognition)
def example_speech_recognizer():
    """Ejemplo de uso del reconocedor de voz"""
    try:
        from core.speech_recognizer import SpeechRecognizer

        def on_text_callback(text):
            print(f"Recognized: {text}")

        # Create recognizer with callback
        recognizer = SpeechRecognizer(callback=on_text_callback)

        # Test microphone
        if recognizer.test_microphone():
            print("Microphone is working!")

        # Recognize once
        print("Say something...")
        text = recognizer.recognize_once()
        if text:
            print(f"You said: {text}")

        # Change language
        recognizer.set_language('en-US')

        # Start continuous listening
        # recognizer.start_listening()
        # ... do other things ...
        # recognizer.stop_listening()

    except ImportError as e:
        print(f"Required module not installed: {e}")


# Example 4: Using CommandProcessor
def example_command_processor():
    """Ejemplo de uso del procesador de comandos"""
    try:
        from core.command_processor import CommandProcessor

        processor = CommandProcessor()

        # Process punctuation command
        text, is_action = processor.process_text("punto")
        print(f"'punto' -> '{text}' (is_action: {is_action})")

        # Process formatting command
        text, is_action = processor.process_text("nueva línea")
        print(f"'nueva línea' -> '{repr(text)}' (is_action: {is_action})")

        # Process regular text
        text, is_action = processor.process_text("Hello world")
        print(f"'Hello world' -> '{text}' (is_action: {is_action})")

        # Add to buffer
        processor.add_to_buffer(text)

        # Get buffer content
        buffer = processor.get_buffer_text()
        print(f"Buffer: {buffer}")

        # Clear buffer
        processor.clear_buffer()

    except ImportError as e:
        print(f"Required module not installed: {e}")


# Example 5: Using HotkeyManager (requires keyboard)
def example_hotkey_manager():
    """Ejemplo de uso del gestor de hotkeys"""
    try:
        from core.hotkey_manager import HotkeyManager

        manager = HotkeyManager()

        # Test if a hotkey is valid
        is_valid = manager.test_hotkey('ctrl+shift+a')
        print(f"'ctrl+shift+a' is valid: {is_valid}")

        # Check if a hotkey is available
        is_available = manager.is_hotkey_available('ctrl+shift+z')
        print(f"'ctrl+shift+z' is available: {is_available}")

        # Normalize hotkey
        normalized = manager.normalize_hotkey('CTRL + SHIFT + A')
        print(f"Normalized: {normalized}")

        # Register a hotkey
        def my_callback():
            print("Hotkey pressed!")

        # Note: This requires running with admin privileges on Windows
        # manager.register_hotkey('ctrl+shift+h', my_callback, "My custom hotkey")

        # Get registered hotkeys
        hotkeys = manager.get_registered_hotkeys()
        print(f"Registered hotkeys: {hotkeys}")

    except ImportError as e:
        print(f"Required module not installed: {e}")


# Example 6: Using Multiple Components Together
def example_complete_workflow():
    """Ejemplo de flujo completo usando múltiples componentes"""
    print("\n=== Complete Workflow Example ===\n")

    try:
        from utils.config import ConfigManager
        from core.command_processor import CommandProcessor

        # 1. Load config
        config = ConfigManager()
        print(f"1. Config loaded - Language: {config.get('language')}")

        # 2. Create command processor
        processor = CommandProcessor()
        print("2. Command processor created")

        # 3. Simulate voice input
        voice_inputs = [
            "Hola mundo",
            "punto",
            "nueva línea",
            "Este es un ejemplo",
            "signo de exclamación"
        ]

        print("\n3. Processing voice inputs:")
        for voice_input in voice_inputs:
            text, is_action = processor.process_text(voice_input)

            if is_action:
                print(f"   Action: {voice_input}")
            elif text:
                processor.add_to_buffer(text)
                print(f"   '{voice_input}' -> '{text}'")

        # 4. Get final text
        final_text = processor.get_buffer_text()
        print(f"\n4. Final text:\n   {repr(final_text)}")

        # 5. Simulated output
        print(f"\n5. Rendered output:\n   {final_text}")

    except ImportError as e:
        print(f"Error: {e}")
        print("Install dependencies with: pip install -r requirements.txt")


# Example 7: Custom Voice Command Handler
def example_custom_command_handler():
    """Ejemplo de manejo personalizado de comandos de voz"""
    from utils.config import ConfigManager

    config = ConfigManager()

    # Define custom handler function
    def handle_voice_command(command: str):
        """Custom handler for voice commands"""
        # Get all commands
        commands = config.get_all_commands()

        # Check punctuation
        if command in commands.get('punctuation_commands', {}):
            return ('punctuation', commands['punctuation_commands'][command])

        # Check formatting
        if command in commands.get('formatting_commands', {}):
            return ('formatting', commands['formatting_commands'][command])

        # Check actions
        if command in commands.get('action_commands', {}):
            return ('action', commands['action_commands'][command])

        # Check custom commands
        for custom_cmd in commands.get('custom_commands', []):
            if custom_cmd.get('trigger', '').lower() == command.lower():
                return ('custom', custom_cmd)

        # Regular text
        return ('text', command)

    # Test the handler
    test_commands = ['punto', 'nueva línea', 'mi correo', 'regular text']

    print("\nCustom Command Handler:")
    for cmd in test_commands:
        cmd_type, result = handle_voice_command(cmd)
        print(f"  '{cmd}' -> Type: {cmd_type}, Result: {result}")


if __name__ == "__main__":
    print("="*60)
    print("Dictado por Voz - API Usage Examples")
    print("="*60)

    examples = [
        ("1. ConfigManager", example_config_manager),
        ("2. ClipboardManager", example_clipboard),
        ("3. SpeechRecognizer", example_speech_recognizer),
        ("4. CommandProcessor", example_command_processor),
        ("5. HotkeyManager", example_hotkey_manager),
        ("6. Complete Workflow", example_complete_workflow),
        ("7. Custom Command Handler", example_custom_command_handler)
    ]

    for name, example_func in examples:
        print(f"\n{name}")
        print("-" * 60)
        try:
            example_func()
        except Exception as e:
            print(f"Error running example: {e}")

    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)
