"""
Unit tests for ClipboardManager
Tests clipboard operations and text insertion
"""

import unittest
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestClipboardManager(unittest.TestCase):
    """Test ClipboardManager functionality"""

    def setUp(self):
        """Set up test fixtures"""
        # We'll test the class structure even without the actual dependencies
        pass

    @patch('utils.clipboard.pyperclip')
    def test_copy_to_clipboard(self, mock_pyperclip):
        """Test copying text to clipboard"""
        from utils.clipboard import ClipboardManager

        mock_pyperclip.copy = Mock()
        result = ClipboardManager.copy_to_clipboard("test text")

        mock_pyperclip.copy.assert_called_once_with("test text")
        self.assertTrue(result)

    @patch('utils.clipboard.pyperclip')
    def test_copy_to_clipboard_error(self, mock_pyperclip):
        """Test handling errors when copying to clipboard"""
        from utils.clipboard import ClipboardManager

        mock_pyperclip.copy.side_effect = Exception("Test error")
        result = ClipboardManager.copy_to_clipboard("test text")

        self.assertFalse(result)

    @patch('utils.clipboard.pyperclip')
    def test_paste_from_clipboard(self, mock_pyperclip):
        """Test getting text from clipboard"""
        from utils.clipboard import ClipboardManager

        mock_pyperclip.paste.return_value = "clipboard content"
        result = ClipboardManager.paste_from_clipboard()

        self.assertEqual(result, "clipboard content")

    @patch('utils.clipboard.pyperclip')
    def test_paste_from_clipboard_error(self, mock_pyperclip):
        """Test handling errors when pasting from clipboard"""
        from utils.clipboard import ClipboardManager

        mock_pyperclip.paste.side_effect = Exception("Test error")
        result = ClipboardManager.paste_from_clipboard()

        self.assertEqual(result, "")

    @patch('utils.clipboard.keyboard')
    @patch('utils.clipboard.pyperclip')
    @patch('utils.clipboard.time')
    def test_insert_text(self, mock_time, mock_pyperclip, mock_keyboard):
        """Test inserting text using clipboard paste"""
        from utils.clipboard import ClipboardManager

        mock_pyperclip.paste.return_value = "original"
        mock_pyperclip.copy = Mock()
        mock_keyboard.send = Mock()

        result = ClipboardManager.insert_text("new text", delay=0.1)

        # Should copy new text
        self.assertTrue(mock_pyperclip.copy.called)
        # Should simulate Ctrl+V
        mock_keyboard.send.assert_called_with('ctrl+v')
        # Should restore original clipboard
        self.assertTrue(result)

    @patch('utils.clipboard.keyboard')
    def test_type_text(self, mock_keyboard):
        """Test typing text character by character"""
        from utils.clipboard import ClipboardManager

        mock_keyboard.write = Mock()
        result = ClipboardManager.type_text("test", delay=0.01)

        mock_keyboard.write.assert_called_once_with("test", delay=0.01)
        self.assertTrue(result)

    @patch('utils.clipboard.keyboard')
    def test_simulate_keypress(self, mock_keyboard):
        """Test simulating keyboard shortcuts"""
        from utils.clipboard import ClipboardManager

        mock_keyboard.send = Mock()
        result = ClipboardManager.simulate_keypress("ctrl+enter")

        mock_keyboard.send.assert_called_once_with("ctrl+enter")
        self.assertTrue(result)

    @patch('utils.clipboard.keyboard')
    @patch('utils.clipboard.time')
    def test_delete_characters(self, mock_time, mock_keyboard):
        """Test deleting characters using backspace"""
        from utils.clipboard import ClipboardManager

        mock_keyboard.send = Mock()
        result = ClipboardManager.delete_characters(5)

        # Should send backspace 5 times
        self.assertEqual(mock_keyboard.send.call_count, 5)
        self.assertTrue(result)

    def test_clipboard_manager_without_keyboard_module(self):
        """Test that ClipboardManager handles missing keyboard module"""
        # This tests the import error handling
        import sys
        with patch.dict('sys.modules', {'keyboard': None}):
            # Should still be able to import
            from utils.clipboard import ClipboardManager
            self.assertIsNotNone(ClipboardManager)


class TestClipboardManagerIntegration(unittest.TestCase):
    """Integration tests for ClipboardManager"""

    @patch('utils.clipboard.pyperclip')
    @patch('utils.clipboard.keyboard')
    def test_full_insert_workflow(self, mock_keyboard, mock_pyperclip):
        """Test complete workflow of inserting text"""
        from utils.clipboard import ClipboardManager

        # Setup mocks
        original_content = "original text"
        mock_pyperclip.paste.return_value = original_content
        mock_pyperclip.copy = Mock()
        mock_keyboard.send = Mock()

        # Insert new text
        new_text = "Hello World"
        result = ClipboardManager.insert_text(new_text, delay=0.0)

        # Verify workflow
        self.assertTrue(result)

        # Check that copy was called with correct arguments
        copy_calls = [call[0][0] for call in mock_pyperclip.copy.call_args_list]
        self.assertIn(new_text, copy_calls)
        self.assertIn(original_content, copy_calls)

        # Check Ctrl+V was sent
        mock_keyboard.send.assert_called_with('ctrl+v')


if __name__ == '__main__':
    unittest.main()
