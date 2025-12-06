"""
Unit tests for HotkeyManager
Tests hotkey registration and management
"""

import unittest
import os
import sys
from unittest.mock import Mock, patch, MagicMock, call

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestHotkeyManager(unittest.TestCase):
    """Test HotkeyManager functionality"""

    def setUp(self):
        """Set up test fixtures"""
        # Mock config to avoid file dependencies
        self.mock_config_data = {
            'hotkeys.toggle_dictation': 'ctrl+shift+space',
            'hotkeys.stop_dictation': 'ctrl+shift+s',
            'hotkeys.open_settings': 'ctrl+shift+o'
        }

    @patch('core.hotkey_manager.keyboard')
    @patch('core.hotkey_manager.config')
    def test_init_loads_hotkeys(self, mock_config, mock_keyboard):
        """Test that HotkeyManager initializes with hotkeys from config"""
        mock_config.get.side_effect = lambda key, default=None: self.mock_config_data.get(key, default)

        from core.hotkey_manager import HotkeyManager
        manager = HotkeyManager()

        self.assertEqual(manager.toggle_dictation_key, 'ctrl+shift+space')
        self.assertEqual(manager.stop_dictation_key, 'ctrl+shift+s')
        self.assertEqual(manager.open_settings_key, 'ctrl+shift+o')

    @patch('core.hotkey_manager.keyboard')
    @patch('core.hotkey_manager.config')
    def test_register_hotkey(self, mock_config, mock_keyboard):
        """Test registering a hotkey"""
        mock_config.get.return_value = 'ctrl+a'
        mock_keyboard.add_hotkey = Mock()

        from core.hotkey_manager import HotkeyManager
        manager = HotkeyManager()

        callback = Mock()
        manager.register_hotkey('ctrl+h', callback, "Test hotkey")

        # Should call keyboard.add_hotkey
        mock_keyboard.add_hotkey.assert_called()
        self.assertIn('ctrl+h', manager.registered_keys)

    @patch('core.hotkey_manager.keyboard')
    @patch('core.hotkey_manager.config')
    def test_unregister_hotkey(self, mock_config, mock_keyboard):
        """Test unregistering a hotkey"""
        mock_config.get.return_value = 'ctrl+a'
        mock_keyboard.add_hotkey = Mock()
        mock_keyboard.remove_hotkey = Mock()

        from core.hotkey_manager import HotkeyManager
        manager = HotkeyManager()

        callback = Mock()
        manager.register_hotkey('ctrl+h', callback)
        manager.unregister_hotkey('ctrl+h')

        # Should call keyboard.remove_hotkey
        mock_keyboard.remove_hotkey.assert_called_with('ctrl+h')
        self.assertNotIn('ctrl+h', manager.registered_keys)

    @patch('core.hotkey_manager.keyboard')
    @patch('core.hotkey_manager.config')
    def test_unregister_all(self, mock_config, mock_keyboard):
        """Test unregistering all hotkeys"""
        mock_config.get.return_value = 'ctrl+a'
        mock_keyboard.add_hotkey = Mock()
        mock_keyboard.remove_hotkey = Mock()

        from core.hotkey_manager import HotkeyManager
        manager = HotkeyManager()

        # Register multiple hotkeys
        manager.register_hotkey('ctrl+h', Mock())
        manager.register_hotkey('ctrl+j', Mock())
        manager.register_hotkey('ctrl+k', Mock())

        manager.unregister_all()

        # All should be removed
        self.assertEqual(len(manager.registered_keys), 0)
        self.assertEqual(mock_keyboard.remove_hotkey.call_count, 3)

    @patch('core.hotkey_manager.keyboard')
    @patch('core.hotkey_manager.config')
    def test_register_default_hotkeys(self, mock_config, mock_keyboard):
        """Test registering default application hotkeys"""
        mock_config.get.side_effect = lambda key, default=None: self.mock_config_data.get(key, default)
        mock_keyboard.add_hotkey = Mock()

        from core.hotkey_manager import HotkeyManager
        manager = HotkeyManager()

        toggle_cb = Mock()
        stop_cb = Mock()
        settings_cb = Mock()

        manager.register_default_hotkeys(toggle_cb, stop_cb, settings_cb)

        # Should have registered 3 hotkeys
        self.assertGreaterEqual(mock_keyboard.add_hotkey.call_count, 3)

    @patch('core.hotkey_manager.keyboard')
    @patch('core.hotkey_manager.config')
    def test_update_hotkey(self, mock_config, mock_keyboard):
        """Test updating a hotkey with new combination"""
        mock_config.get.return_value = 'ctrl+a'
        mock_config.set = Mock()
        mock_keyboard.add_hotkey = Mock()
        mock_keyboard.remove_hotkey = Mock()

        from core.hotkey_manager import HotkeyManager
        manager = HotkeyManager()
        manager.toggle_dictation_key = 'ctrl+shift+space'
        manager.registered_keys.add('ctrl+shift+space')

        callback = Mock()
        manager.update_hotkey('toggle_dictation', 'ctrl+alt+t', callback)

        # Should have removed old and registered new
        mock_keyboard.remove_hotkey.assert_called()
        mock_keyboard.add_hotkey.assert_called()
        # Should have saved to config
        mock_config.set.assert_called()

    @patch('core.hotkey_manager.keyboard')
    @patch('core.hotkey_manager.config')
    def test_is_hotkey_available(self, mock_config, mock_keyboard):
        """Test checking if hotkey combination is available"""
        mock_config.get.return_value = 'ctrl+a'
        mock_keyboard.add_hotkey = Mock()

        from core.hotkey_manager import HotkeyManager
        manager = HotkeyManager()

        manager.register_hotkey('ctrl+h', Mock())

        self.assertFalse(manager.is_hotkey_available('ctrl+h'))
        self.assertTrue(manager.is_hotkey_available('ctrl+j'))

    @patch('core.hotkey_manager.keyboard')
    @patch('core.hotkey_manager.config')
    def test_test_hotkey_valid(self, mock_config, mock_keyboard):
        """Test validating a hotkey combination"""
        mock_config.get.return_value = 'ctrl+a'
        mock_keyboard.parse_hotkey = Mock(return_value=[])

        from core.hotkey_manager import HotkeyManager
        manager = HotkeyManager()

        result = manager.test_hotkey('ctrl+shift+a')

        mock_keyboard.parse_hotkey.assert_called_with('ctrl+shift+a')
        self.assertTrue(result)

    @patch('core.hotkey_manager.keyboard')
    @patch('core.hotkey_manager.config')
    def test_test_hotkey_invalid(self, mock_config, mock_keyboard):
        """Test validating an invalid hotkey combination"""
        mock_config.get.return_value = 'ctrl+a'
        mock_keyboard.parse_hotkey.side_effect = Exception("Invalid hotkey")

        from core.hotkey_manager import HotkeyManager
        manager = HotkeyManager()

        result = manager.test_hotkey('invalid+++key')

        self.assertFalse(result)

    @patch('core.hotkey_manager.keyboard')
    @patch('core.hotkey_manager.config')
    def test_normalize_hotkey(self, mock_config, mock_keyboard):
        """Test normalizing hotkey format"""
        mock_config.get.return_value = 'ctrl+a'
        mock_keyboard.parse_hotkey.return_value = []
        mock_keyboard.get_hotkey_name.return_value = 'ctrl+shift+a'

        from core.hotkey_manager import HotkeyManager
        manager = HotkeyManager()

        result = manager.normalize_hotkey('CTRL + SHIFT + A')

        self.assertEqual(result, 'ctrl+shift+a')

    @patch('core.hotkey_manager.keyboard')
    @patch('core.hotkey_manager.config')
    def test_get_registered_hotkeys(self, mock_config, mock_keyboard):
        """Test getting all registered hotkeys"""
        mock_config.get.side_effect = lambda key, default=None: self.mock_config_data.get(key, default)

        from core.hotkey_manager import HotkeyManager
        manager = HotkeyManager()

        hotkeys = manager.get_registered_hotkeys()

        self.assertIsInstance(hotkeys, dict)
        self.assertIn('toggle_dictation', hotkeys)
        self.assertIn('stop_dictation', hotkeys)
        self.assertIn('open_settings', hotkeys)

    @patch('core.hotkey_manager.keyboard')
    @patch('core.hotkey_manager.config')
    def test_register_hotkey_error_handling(self, mock_config, mock_keyboard):
        """Test error handling when registering hotkey fails"""
        mock_config.get.return_value = 'ctrl+a'
        mock_keyboard.add_hotkey.side_effect = Exception("Registration failed")

        from core.hotkey_manager import HotkeyManager
        manager = HotkeyManager()

        # Should not raise exception
        manager.register_hotkey('ctrl+h', Mock())

        # Hotkey should not be in registered keys
        self.assertNotIn('ctrl+h', manager.registered_keys)


if __name__ == '__main__':
    unittest.main()
