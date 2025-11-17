"""
Unit tests for CommandProcessor
Tests command processing, text formatting, and actions
"""

import unittest
import os
import sys
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.command_processor import CommandProcessor


class TestCommandProcessor(unittest.TestCase):
    """Test CommandProcessor functionality"""

    def setUp(self):
        """Set up test fixtures"""
        # Mock the config to avoid file dependencies
        self.mock_config_data = {
            "punctuation_commands": {
                "punto": ".",
                "coma": ",",
                "interrogación": "?",
                "exclamación": "!",
                "period": ".",
                "comma": ","
            },
            "formatting_commands": {
                "nueva línea": "\n",
                "nuevo párrafo": "\n\n",
                "tabulación": "\t",
                "new line": "\n"
            },
            "action_commands": {
                "borrar última palabra": {
                    "action": "delete_last_word",
                    "params": 1
                },
                "borrar todo": {
                    "action": "clear_buffer"
                },
                "detener dictado": {
                    "action": "stop_dictation"
                }
            },
            "custom_commands": [
                {
                    "id": "test_email",
                    "enabled": True,
                    "trigger": "mi correo",
                    "action": "insert_text",
                    "value": "test@example.com"
                },
                {
                    "id": "test_date",
                    "enabled": True,
                    "trigger": "fecha actual",
                    "action": "insert_date",
                    "format": "%d/%m/%Y"
                }
            ]
        }

        # Patch config
        with patch('core.command_processor.config') as mock_config:
            mock_config.get_all_commands.return_value = self.mock_config_data
            mock_config.get.return_value = True
            self.processor = CommandProcessor()
            # Set the commands manually since we're mocking
            self.processor.commands = self.mock_config_data
            self.processor.punctuation_commands = self.mock_config_data['punctuation_commands']
            self.processor.formatting_commands = self.mock_config_data['formatting_commands']
            self.processor.action_commands = self.mock_config_data['action_commands']
            self.processor.custom_commands = self.mock_config_data['custom_commands']

    def test_process_punctuation_command_spanish(self):
        """Test processing Spanish punctuation commands"""
        text, is_action = self.processor.process_text("punto")

        self.assertEqual(text, ".")
        self.assertFalse(is_action)

    def test_process_punctuation_command_english(self):
        """Test processing English punctuation commands"""
        text, is_action = self.processor.process_text("period")

        self.assertEqual(text, ".")
        self.assertFalse(is_action)

    def test_process_formatting_command(self):
        """Test processing formatting commands"""
        text, is_action = self.processor.process_text("nueva línea")

        self.assertEqual(text, "\n")
        self.assertFalse(is_action)

    def test_process_action_command(self):
        """Test processing action commands"""
        text, is_action = self.processor.process_text("borrar todo")

        self.assertIsNone(text)
        self.assertTrue(is_action)

    def test_process_custom_command_insert_text(self):
        """Test custom command that inserts text"""
        text, is_action = self.processor.process_text("mi correo")

        self.assertEqual(text, "test@example.com")
        self.assertFalse(is_action)

    def test_process_custom_command_insert_date(self):
        """Test custom command that inserts current date"""
        text, is_action = self.processor.process_text("fecha actual")

        # Should match format DD/MM/YYYY
        self.assertIsNotNone(text)
        self.assertFalse(is_action)
        # Verify it's a valid date format
        parts = text.split('/')
        self.assertEqual(len(parts), 3)

    def test_process_regular_text(self):
        """Test processing regular text (not a command)"""
        text, is_action = self.processor.process_text("hello world")

        self.assertIn("hello world", text.lower())
        self.assertFalse(is_action)

    def test_auto_capitalization_first_word(self):
        """Test that first word is capitalized"""
        self.processor.auto_capitalization = True
        self.processor.text_buffer = []

        text, _ = self.processor.process_text("hello")

        # First letter should be capitalized
        self.assertTrue(text[0].isupper())

    def test_auto_capitalization_after_period(self):
        """Test capitalization after sentence-ending punctuation"""
        self.processor.auto_capitalization = True
        self.processor.text_buffer = ["Test."]

        text, _ = self.processor.process_text("hello")

        # Should be capitalized after period
        self.assertTrue(text.strip()[0].isupper())

    def test_add_to_buffer(self):
        """Test adding text to buffer"""
        self.processor.add_to_buffer("Hello")
        self.processor.add_to_buffer(" ")
        self.processor.add_to_buffer("World")

        buffer = self.processor.get_buffer_text()
        self.assertEqual(buffer, "Hello World")

    def test_clear_buffer(self):
        """Test clearing the buffer"""
        self.processor.add_to_buffer("Test text")
        self.processor.clear_buffer()

        buffer = self.processor.get_buffer_text()
        self.assertEqual(buffer, "")

    def test_get_buffer_text(self):
        """Test getting complete buffer text"""
        self.processor.text_buffer = ["Hello", " ", "World", "!"]

        buffer = self.processor.get_buffer_text()
        self.assertEqual(buffer, "Hello World!")

    def test_case_insensitive_commands(self):
        """Test that commands are case-insensitive"""
        text1, _ = self.processor.process_text("punto")
        text2, _ = self.processor.process_text("PUNTO")
        text3, _ = self.processor.process_text("Punto")

        self.assertEqual(text1, text2)
        self.assertEqual(text2, text3)

    def test_empty_text_processing(self):
        """Test processing empty or None text"""
        text, is_action = self.processor.process_text("")

        self.assertIsNone(text)
        self.assertFalse(is_action)

    def test_whitespace_handling(self):
        """Test that whitespace is properly handled"""
        text, _ = self.processor.process_text("  hello  ")

        # Should be trimmed
        self.assertFalse(text.startswith("  "))

    def test_multiple_commands_sequence(self):
        """Test processing a sequence of commands"""
        commands = [
            ("Hola", False),
            ("punto", False),
            ("nueva línea", False),
            ("Mundo", False)
        ]

        results = []
        for cmd, _ in commands:
            text, is_action = self.processor.process_text(cmd)
            if not is_action and text:
                self.processor.add_to_buffer(text)
                results.append(text)

        # Check buffer contains all processed text
        buffer = self.processor.get_buffer_text()
        self.assertIn("Hola", buffer)
        self.assertIn(".", buffer)

    @patch('core.command_processor.ClipboardManager')
    def test_insert_text_auto_insert(self, mock_clipboard_class):
        """Test inserting text with auto_insert enabled"""
        mock_clipboard = Mock()
        mock_clipboard_class.return_value = mock_clipboard
        mock_clipboard.type_text.return_value = True

        # Create new processor with mocked clipboard
        with patch('core.command_processor.config') as mock_config:
            mock_config.get_all_commands.return_value = self.mock_config_data
            mock_config.get.side_effect = lambda key, default=None: {
                'output.auto_insert': True,
                'output.use_clipboard': False,
                'advanced.auto_punctuation': True,
                'advanced.auto_capitalization': True,
                'advanced.enable_custom_commands': True
            }.get(key, default)

            processor = CommandProcessor()
            result = processor.insert_text("test text")

            # Should have called type_text
            self.assertTrue(mock_clipboard.type_text.called)

    def test_reload_commands(self):
        """Test reloading commands from config"""
        with patch('core.command_processor.config') as mock_config:
            new_commands = {
                "punctuation_commands": {"new": "!"},
                "formatting_commands": {},
                "action_commands": {},
                "custom_commands": []
            }
            mock_config.get_all_commands.return_value = new_commands

            self.processor.reload_commands()

            # Commands should be reloaded
            self.assertEqual(self.processor.punctuation_commands, {"new": "!"})


class TestCommandProcessorActions(unittest.TestCase):
    """Test action commands specifically"""

    def setUp(self):
        """Set up test fixtures"""
        mock_config_data = {
            "punctuation_commands": {},
            "formatting_commands": {},
            "action_commands": {
                "borrar última palabra": {
                    "action": "delete_last_word",
                    "params": 1
                },
                "borrar todo": {
                    "action": "clear_buffer"
                }
            },
            "custom_commands": []
        }

        with patch('core.command_processor.config') as mock_config:
            mock_config.get_all_commands.return_value = mock_config_data
            mock_config.get.return_value = True
            self.processor = CommandProcessor()
            self.processor.commands = mock_config_data
            self.processor.action_commands = mock_config_data['action_commands']

    def test_action_clear_buffer(self):
        """Test clear buffer action command"""
        self.processor.add_to_buffer("Test text")

        # Execute clear buffer command
        self.processor._execute_action_command("borrar todo")

        buffer = self.processor.get_buffer_text()
        self.assertEqual(buffer, "")

    @patch('core.command_processor.ClipboardManager')
    def test_action_delete_last_word(self, mock_clipboard_class):
        """Test delete last word action"""
        mock_clipboard = Mock()
        mock_clipboard_class.return_value = mock_clipboard

        self.processor.text_buffer = ["Hello World"]
        self.processor._execute_action_command("borrar última palabra")

        # Should have called delete_characters
        self.assertTrue(mock_clipboard.delete_characters.called)


if __name__ == '__main__':
    unittest.main()
