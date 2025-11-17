"""
Command processor module
Handles processing of voice commands, punctuation, and text formatting
"""

import re
import webbrowser
from datetime import datetime
from typing import Optional, Tuple
from ..utils.config import config
from ..utils.clipboard import ClipboardManager


class CommandProcessor:
    """Processes voice commands and formats text"""

    def __init__(self):
        """Initialize command processor"""
        self.clipboard = ClipboardManager()
        self.text_buffer = []
        self.commands = config.get_all_commands()

        # Load commands
        self.punctuation_commands = self.commands.get('punctuation_commands', {})
        self.formatting_commands = self.commands.get('formatting_commands', {})
        self.action_commands = self.commands.get('action_commands', {})
        self.custom_commands = self.commands.get('custom_commands', [])

        # Settings
        self.auto_punctuation = config.get('advanced.auto_punctuation', True)
        self.auto_capitalization = config.get('advanced.auto_capitalization', True)
        self.enable_custom_commands = config.get('advanced.enable_custom_commands', True)

    def process_text(self, text: str) -> Tuple[Optional[str], bool]:
        """
        Process recognized text and check for commands

        Args:
            text: Recognized text from speech

        Returns:
            Tuple of (processed_text, is_action_command)
            - processed_text: Text to insert (or None if action command)
            - is_action_command: True if this was an action command
        """
        if not text:
            return None, False

        text = text.strip()
        lower_text = text.lower()

        # Check action commands first
        if lower_text in self.action_commands:
            self._execute_action_command(lower_text)
            return None, True

        # Check custom commands
        if self.enable_custom_commands:
            custom_result = self._check_custom_commands(text)
            if custom_result is not None:
                return custom_result, False

        # Check formatting commands
        if lower_text in self.formatting_commands:
            formatted = self.formatting_commands[lower_text]
            return formatted, False

        # Check punctuation commands
        if lower_text in self.punctuation_commands:
            punct = self.punctuation_commands[lower_text]
            return punct, False

        # Apply auto-capitalization and formatting
        processed = self._apply_formatting(text)

        return processed, False

    def _check_custom_commands(self, text: str) -> Optional[str]:
        """
        Check if text matches any custom command

        Args:
            text: Text to check

        Returns:
            str: Command result or None
        """
        lower_text = text.lower()

        for command in self.custom_commands:
            if not command.get('enabled', True):
                continue

            # Check main trigger
            trigger = command.get('trigger', '').lower()
            if lower_text == trigger:
                return self._execute_custom_command(command)

            # Check alternatives
            alternatives = command.get('alternatives', [])
            for alt in alternatives:
                if lower_text == alt.lower():
                    return self._execute_custom_command(command)

        return None

    def _execute_custom_command(self, command: dict) -> Optional[str]:
        """
        Execute a custom command

        Args:
            command: Command dictionary

        Returns:
            str: Result text or None for actions
        """
        action = command.get('action')
        value = command.get('value')

        if action == 'insert_text':
            return value

        elif action == 'insert_date':
            date_format = command.get('format', '%d/%m/%Y')
            return datetime.now().strftime(date_format)

        elif action == 'insert_time':
            time_format = command.get('format', '%H:%M')
            return datetime.now().strftime(time_format)

        elif action == 'open_url':
            try:
                webbrowser.open(value)
            except Exception as e:
                print(f"Error opening URL: {e}")
            return None

        elif action == 'press_key':
            self.clipboard.simulate_keypress(value)
            return None

        return None

    def _execute_action_command(self, command: str):
        """
        Execute an action command

        Args:
            command: Command to execute
        """
        cmd_data = self.action_commands.get(command, {})
        action = cmd_data.get('action')

        if action == 'delete_last_word':
            self._delete_last_words(1)

        elif action == 'delete_last_words':
            # Extract number from speech (e.g., "borrar últimas 3 palabras")
            # For now, delete last word
            self._delete_last_words(1)

        elif action == 'clear_buffer':
            self.text_buffer.clear()
            print("Buffer cleared")

        elif action == 'stop_dictation':
            # This will be handled by the main app
            print("Stop dictation command received")

        elif action == 'pause_dictation':
            print("Pause dictation command received")

        elif action == 'resume_dictation':
            print("Resume dictation command received")

    def _delete_last_words(self, count: int):
        """
        Delete last N words from buffer

        Args:
            count: Number of words to delete
        """
        if not self.text_buffer:
            return

        # Get last inserted text
        if self.text_buffer:
            last_text = self.text_buffer[-1]
            words = last_text.split()

            if len(words) <= count:
                # Remove entire last entry
                self.text_buffer.pop()
                char_count = len(last_text)
            else:
                # Remove N words
                words = words[:-count]
                new_text = ' '.join(words)
                self.text_buffer[-1] = new_text
                char_count = len(last_text) - len(new_text)

            # Delete characters from active application
            self.clipboard.delete_characters(char_count)

    def _apply_formatting(self, text: str) -> str:
        """
        Apply automatic formatting to text

        Args:
            text: Text to format

        Returns:
            str: Formatted text
        """
        if not text:
            return text

        # Auto-capitalization
        if self.auto_capitalization and self.text_buffer:
            # Capitalize first letter if previous text ended with sentence-ending punctuation
            if self.text_buffer:
                last_text = self.text_buffer[-1]
                if last_text and last_text[-1] in '.!?':
                    text = text[0].upper() + text[1:] if len(text) > 1 else text.upper()
        elif self.auto_capitalization and not self.text_buffer:
            # Capitalize first word of session
            text = text[0].upper() + text[1:] if len(text) > 1 else text.upper()

        # Add space before text if buffer is not empty
        if self.text_buffer and self.text_buffer[-1] and not self.text_buffer[-1].endswith(('\n', ' ')):
            text = ' ' + text

        return text

    def add_to_buffer(self, text: str):
        """
        Add text to buffer

        Args:
            text: Text to add
        """
        self.text_buffer.append(text)

    def get_buffer_text(self) -> str:
        """
        Get all text from buffer

        Returns:
            str: Complete buffer text
        """
        return ''.join(self.text_buffer)

    def clear_buffer(self):
        """Clear the text buffer"""
        self.text_buffer.clear()

    def insert_text(self, text: str) -> bool:
        """
        Insert text into active application

        Args:
            text: Text to insert

        Returns:
            bool: True if successful
        """
        auto_insert = config.get('output.auto_insert', True)
        use_clipboard = config.get('output.use_clipboard', False)
        paste_delay = config.get('output.paste_delay', 0.1)

        if auto_insert:
            if use_clipboard:
                return self.clipboard.insert_text(text, delay=paste_delay)
            else:
                return self.clipboard.type_text(text)
        else:
            # Just copy to clipboard
            return self.clipboard.copy_to_clipboard(text)

    def reload_commands(self):
        """Reload commands from config"""
        self.commands = config.get_all_commands()
        self.punctuation_commands = self.commands.get('punctuation_commands', {})
        self.formatting_commands = self.commands.get('formatting_commands', {})
        self.action_commands = self.commands.get('action_commands', {})
        self.custom_commands = self.commands.get('custom_commands', [])
