"""
Configuration management module
Handles loading and saving of application settings
"""

import json
import os
from pathlib import Path
from typing import Any, Dict


class ConfigManager:
    """Manages application configuration"""

    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.config_dir = self.base_dir / "config"
        self.settings_file = self.config_dir / "settings.json"
        self.commands_file = self.config_dir / "commands.json"

        self.settings = {}
        self.commands = {}

        self.load_config()

    def load_config(self):
        """Load configuration from JSON files"""
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            print(f"Settings file not found: {self.settings_file}")
            self.settings = self._get_default_settings()
            self.save_settings()
        except json.JSONDecodeError as e:
            print(f"Error parsing settings file: {e}")
            self.settings = self._get_default_settings()

        try:
            with open(self.commands_file, 'r', encoding='utf-8') as f:
                self.commands = json.load(f)
        except FileNotFoundError:
            print(f"Commands file not found: {self.commands_file}")
            self.commands = self._get_default_commands()
            self.save_commands()
        except json.JSONDecodeError as e:
            print(f"Error parsing commands file: {e}")
            self.commands = self._get_default_commands()

    def save_settings(self):
        """Save settings to JSON file"""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def save_commands(self):
        """Save commands to JSON file"""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.commands_file, 'w', encoding='utf-8') as f:
                json.dump(self.commands, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving commands: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value using dot notation (e.g., 'recognition.engine')"""
        keys = key.split('.')
        value = self.settings

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """Set a setting value using dot notation"""
        keys = key.split('.')
        target = self.settings

        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]

        target[keys[-1]] = value
        self.save_settings()

    def get_command(self, command_type: str) -> Dict:
        """Get commands of a specific type"""
        return self.commands.get(command_type, {})

    def get_all_commands(self) -> Dict:
        """Get all commands"""
        return self.commands

    def add_custom_command(self, command: Dict):
        """Add a new custom command"""
        if "custom_commands" not in self.commands:
            self.commands["custom_commands"] = []

        self.commands["custom_commands"].append(command)
        self.save_commands()

    def remove_custom_command(self, command_id: str):
        """Remove a custom command by ID"""
        if "custom_commands" in self.commands:
            self.commands["custom_commands"] = [
                cmd for cmd in self.commands["custom_commands"]
                if cmd.get("id") != command_id
            ]
            self.save_commands()

    def update_custom_command(self, command_id: str, updated_command: Dict):
        """Update an existing custom command"""
        if "custom_commands" in self.commands:
            for i, cmd in enumerate(self.commands["custom_commands"]):
                if cmd.get("id") == command_id:
                    self.commands["custom_commands"][i] = updated_command
                    self.save_commands()
                    return True
        return False

    def _get_default_settings(self) -> Dict:
        """Return default settings"""
        return {
            "version": "1.0.0",
            "language": "es-ES",
            "recognition": {
                "engine": "windows",
                "confidence_threshold": 0.7,
                "energy_threshold": 4000
            },
            "hotkeys": {
                "toggle_dictation": "ctrl+shift+space"
            },
            "output": {
                "auto_insert": True
            },
            "ui": {
                "show_main_window": True,
                "minimize_to_tray": True
            }
        }

    def _get_default_commands(self) -> Dict:
        """Return default commands"""
        return {
            "punctuation_commands": {},
            "formatting_commands": {},
            "action_commands": {},
            "custom_commands": []
        }


# Global config instance
config = ConfigManager()
