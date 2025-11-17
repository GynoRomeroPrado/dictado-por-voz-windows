"""
Unit tests for ConfigManager
Tests configuration loading, saving, and management
"""

import unittest
import json
import os
import sys
from pathlib import Path
import tempfile
import shutil

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.config import ConfigManager


class TestConfigManager(unittest.TestCase):
    """Test ConfigManager functionality"""

    def setUp(self):
        """Set up test fixtures"""
        # Create temporary directory for test configs
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = os.path.join(self.test_dir, 'config')
        os.makedirs(self.config_dir, exist_ok=True)

        # Create test settings file
        self.test_settings = {
            "version": "1.0.0",
            "language": "es-ES",
            "recognition": {
                "engine": "google",
                "confidence_threshold": 0.7
            },
            "hotkeys": {
                "toggle_dictation": "ctrl+shift+space"
            }
        }

        self.settings_file = os.path.join(self.config_dir, 'settings.json')
        with open(self.settings_file, 'w') as f:
            json.dump(self.test_settings, f)

        # Create test commands file
        self.test_commands = {
            "punctuation_commands": {
                "punto": ".",
                "coma": ","
            },
            "custom_commands": []
        }

        self.commands_file = os.path.join(self.config_dir, 'commands.json')
        with open(self.commands_file, 'w') as f:
            json.dump(self.test_commands, f)

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_dir)

    def test_init_creates_config_manager(self):
        """Test that ConfigManager initializes correctly"""
        config = ConfigManager()
        self.assertIsNotNone(config)
        self.assertIsInstance(config.settings, dict)
        self.assertIsInstance(config.commands, dict)

    def test_get_setting_simple(self):
        """Test getting a simple setting"""
        config = ConfigManager()
        # Manually set settings for testing
        config.settings = self.test_settings

        version = config.get('version')
        self.assertEqual(version, '1.0.0')

    def test_get_setting_nested(self):
        """Test getting a nested setting using dot notation"""
        config = ConfigManager()
        config.settings = self.test_settings

        engine = config.get('recognition.engine')
        self.assertEqual(engine, 'google')

    def test_get_setting_with_default(self):
        """Test getting a non-existent setting returns default"""
        config = ConfigManager()
        config.settings = self.test_settings

        result = config.get('nonexistent.key', 'default_value')
        self.assertEqual(result, 'default_value')

    def test_set_setting_simple(self):
        """Test setting a simple value"""
        config = ConfigManager()
        config.settings = {}

        config.set('language', 'en-US')
        self.assertEqual(config.settings['language'], 'en-US')

    def test_set_setting_nested(self):
        """Test setting a nested value using dot notation"""
        config = ConfigManager()
        config.settings = {}

        config.set('recognition.engine', 'sphinx')
        self.assertIn('recognition', config.settings)
        self.assertEqual(config.settings['recognition']['engine'], 'sphinx')

    def test_get_command(self):
        """Test getting commands of a specific type"""
        config = ConfigManager()
        config.commands = self.test_commands

        punct_commands = config.get_command('punctuation_commands')
        self.assertIsInstance(punct_commands, dict)
        self.assertEqual(punct_commands['punto'], '.')

    def test_add_custom_command(self):
        """Test adding a custom command"""
        config = ConfigManager()
        config.commands = self.test_commands.copy()

        new_command = {
            "id": "test_cmd",
            "trigger": "test",
            "action": "insert_text",
            "value": "test text"
        }

        config.add_custom_command(new_command)
        self.assertIn(new_command, config.commands['custom_commands'])

    def test_remove_custom_command(self):
        """Test removing a custom command"""
        config = ConfigManager()
        config.commands = {
            "custom_commands": [
                {"id": "cmd1", "trigger": "test1"},
                {"id": "cmd2", "trigger": "test2"}
            ]
        }

        config.remove_custom_command("cmd1")
        self.assertEqual(len(config.commands['custom_commands']), 1)
        self.assertEqual(config.commands['custom_commands'][0]['id'], 'cmd2')

    def test_update_custom_command(self):
        """Test updating an existing custom command"""
        config = ConfigManager()
        config.commands = {
            "custom_commands": [
                {"id": "cmd1", "trigger": "old", "value": "old text"}
            ]
        }

        updated = {"id": "cmd1", "trigger": "new", "value": "new text"}
        result = config.update_custom_command("cmd1", updated)

        self.assertTrue(result)
        self.assertEqual(config.commands['custom_commands'][0]['trigger'], 'new')

    def test_default_settings_structure(self):
        """Test that default settings have correct structure"""
        config = ConfigManager()
        defaults = config._get_default_settings()

        self.assertIn('version', defaults)
        self.assertIn('language', defaults)
        self.assertIn('recognition', defaults)
        self.assertIn('hotkeys', defaults)

    def test_default_commands_structure(self):
        """Test that default commands have correct structure"""
        config = ConfigManager()
        defaults = config._get_default_commands()

        self.assertIn('punctuation_commands', defaults)
        self.assertIn('formatting_commands', defaults)
        self.assertIn('action_commands', defaults)
        self.assertIn('custom_commands', defaults)


class TestConfigManagerIntegration(unittest.TestCase):
    """Integration tests for ConfigManager with actual files"""

    def test_load_actual_config(self):
        """Test loading actual configuration files if they exist"""
        # This assumes the project config files exist
        project_root = os.path.join(os.path.dirname(__file__), '..')
        settings_path = os.path.join(project_root, 'config', 'settings.json')

        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f:
                data = json.load(f)

            # Validate structure
            self.assertIn('version', data)
            self.assertIn('language', data)
            self.assertIsInstance(data['language'], str)

    def test_load_actual_commands(self):
        """Test loading actual commands file if it exists"""
        project_root = os.path.join(os.path.dirname(__file__), '..')
        commands_path = os.path.join(project_root, 'config', 'commands.json')

        if os.path.exists(commands_path):
            with open(commands_path, 'r') as f:
                data = json.load(f)

            # Validate structure
            self.assertIn('punctuation_commands', data)
            self.assertIn('custom_commands', data)
            self.assertIsInstance(data['punctuation_commands'], dict)
            self.assertIsInstance(data['custom_commands'], list)


if __name__ == '__main__':
    unittest.main()
