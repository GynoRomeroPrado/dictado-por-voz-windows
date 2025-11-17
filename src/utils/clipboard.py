"""
Clipboard utilities for text insertion
"""

import pyperclip
import time
try:
    import keyboard
except ImportError:
    keyboard = None


class ClipboardManager:
    """Manages clipboard operations and text insertion"""

    @staticmethod
    def copy_to_clipboard(text: str) -> bool:
        """
        Copy text to clipboard

        Args:
            text: Text to copy

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            print(f"Error copying to clipboard: {e}")
            return False

    @staticmethod
    def paste_from_clipboard() -> str:
        """
        Get text from clipboard

        Returns:
            str: Clipboard content
        """
        try:
            return pyperclip.paste()
        except Exception as e:
            print(f"Error pasting from clipboard: {e}")
            return ""

    @staticmethod
    def insert_text(text: str, delay: float = 0.1) -> bool:
        """
        Insert text into the active application using clipboard paste

        Args:
            text: Text to insert
            delay: Delay before pasting (seconds)

        Returns:
            bool: True if successful, False otherwise
        """
        if not keyboard:
            print("keyboard module not available")
            return False

        try:
            # Save current clipboard content
            original_clipboard = pyperclip.paste()

            # Copy new text to clipboard
            pyperclip.copy(text)

            # Small delay to ensure clipboard is updated
            time.sleep(delay)

            # Simulate Ctrl+V to paste
            keyboard.send('ctrl+v')

            # Small delay before restoring clipboard
            time.sleep(delay)

            # Restore original clipboard content
            pyperclip.copy(original_clipboard)

            return True

        except Exception as e:
            print(f"Error inserting text: {e}")
            return False

    @staticmethod
    def type_text(text: str, delay: float = 0.01) -> bool:
        """
        Type text character by character (alternative to paste)

        Args:
            text: Text to type
            delay: Delay between characters (seconds)

        Returns:
            bool: True if successful, False otherwise
        """
        if not keyboard:
            print("keyboard module not available")
            return False

        try:
            keyboard.write(text, delay=delay)
            return True
        except Exception as e:
            print(f"Error typing text: {e}")
            return False

    @staticmethod
    def simulate_keypress(key_combination: str) -> bool:
        """
        Simulate a keyboard shortcut

        Args:
            key_combination: Key combination (e.g., 'ctrl+enter', 'alt+tab')

        Returns:
            bool: True if successful, False otherwise
        """
        if not keyboard:
            print("keyboard module not available")
            return False

        try:
            keyboard.send(key_combination)
            return True
        except Exception as e:
            print(f"Error simulating keypress: {e}")
            return False

    @staticmethod
    def delete_characters(count: int) -> bool:
        """
        Delete specified number of characters using backspace

        Args:
            count: Number of characters to delete

        Returns:
            bool: True if successful, False otherwise
        """
        if not keyboard:
            print("keyboard module not available")
            return False

        try:
            for _ in range(count):
                keyboard.send('backspace')
                time.sleep(0.01)
            return True
        except Exception as e:
            print(f"Error deleting characters: {e}")
            return False
