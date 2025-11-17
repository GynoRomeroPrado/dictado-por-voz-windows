"""
Hotkey manager module
Handles global keyboard shortcuts for the application
"""

import keyboard
from typing import Callable, Dict, Optional
from ..utils.config import config


class HotkeyManager:
    """Manages global keyboard shortcuts"""

    def __init__(self):
        """Initialize hotkey manager"""
        self.hotkeys: Dict[str, Callable] = {}
        self.registered_keys = set()

        # Load hotkeys from config
        self.toggle_dictation_key = config.get('hotkeys.toggle_dictation', 'ctrl+shift+space')
        self.stop_dictation_key = config.get('hotkeys.stop_dictation', 'ctrl+shift+s')
        self.open_settings_key = config.get('hotkeys.open_settings', 'ctrl+shift+o')

    def register_hotkey(self, key_combination: str, callback: Callable, description: str = ""):
        """
        Register a global hotkey

        Args:
            key_combination: Key combination (e.g., 'ctrl+shift+space')
            callback: Function to call when hotkey is pressed
            description: Description of the hotkey
        """
        try:
            # Remove existing hotkey if registered
            if key_combination in self.registered_keys:
                self.unregister_hotkey(key_combination)

            # Register new hotkey
            keyboard.add_hotkey(key_combination, callback, suppress=True)
            self.hotkeys[key_combination] = callback
            self.registered_keys.add(key_combination)

            print(f"Registered hotkey: {key_combination} - {description}")

        except Exception as e:
            print(f"Error registering hotkey {key_combination}: {e}")

    def unregister_hotkey(self, key_combination: str):
        """
        Unregister a global hotkey

        Args:
            key_combination: Key combination to unregister
        """
        try:
            if key_combination in self.registered_keys:
                keyboard.remove_hotkey(key_combination)
                self.registered_keys.remove(key_combination)
                if key_combination in self.hotkeys:
                    del self.hotkeys[key_combination]
                print(f"Unregistered hotkey: {key_combination}")

        except Exception as e:
            print(f"Error unregistering hotkey {key_combination}: {e}")

    def unregister_all(self):
        """Unregister all hotkeys"""
        for key in list(self.registered_keys):
            self.unregister_hotkey(key)

    def register_default_hotkeys(self, toggle_callback: Callable,
                                 stop_callback: Optional[Callable] = None,
                                 settings_callback: Optional[Callable] = None):
        """
        Register default application hotkeys

        Args:
            toggle_callback: Callback for toggle dictation
            stop_callback: Callback for stop dictation
            settings_callback: Callback for opening settings
        """
        # Toggle dictation
        self.register_hotkey(
            self.toggle_dictation_key,
            toggle_callback,
            "Toggle voice dictation"
        )

        # Stop dictation
        if stop_callback:
            self.register_hotkey(
                self.stop_dictation_key,
                stop_callback,
                "Stop voice dictation"
            )

        # Open settings
        if settings_callback:
            self.register_hotkey(
                self.open_settings_key,
                settings_callback,
                "Open settings"
            )

    def update_hotkey(self, hotkey_name: str, new_combination: str, callback: Callable):
        """
        Update a hotkey with a new key combination

        Args:
            hotkey_name: Name of the hotkey ('toggle_dictation', 'stop_dictation', etc.)
            new_combination: New key combination
            callback: Callback function
        """
        # Get old combination
        old_combination = None
        if hotkey_name == 'toggle_dictation':
            old_combination = self.toggle_dictation_key
            self.toggle_dictation_key = new_combination
            config.set('hotkeys.toggle_dictation', new_combination)

        elif hotkey_name == 'stop_dictation':
            old_combination = self.stop_dictation_key
            self.stop_dictation_key = new_combination
            config.set('hotkeys.stop_dictation', new_combination)

        elif hotkey_name == 'open_settings':
            old_combination = self.open_settings_key
            self.open_settings_key = new_combination
            config.set('hotkeys.open_settings', new_combination)

        # Unregister old and register new
        if old_combination:
            self.unregister_hotkey(old_combination)

        self.register_hotkey(new_combination, callback, hotkey_name)

    def is_hotkey_available(self, key_combination: str) -> bool:
        """
        Check if a key combination is available (not already registered)

        Args:
            key_combination: Key combination to check

        Returns:
            bool: True if available, False if already in use
        """
        return key_combination not in self.registered_keys

    def get_registered_hotkeys(self) -> Dict[str, str]:
        """
        Get all registered hotkeys

        Returns:
            dict: Dictionary of hotkey names and their key combinations
        """
        return {
            'toggle_dictation': self.toggle_dictation_key,
            'stop_dictation': self.stop_dictation_key,
            'open_settings': self.open_settings_key
        }

    def test_hotkey(self, key_combination: str) -> bool:
        """
        Test if a key combination is valid

        Args:
            key_combination: Key combination to test

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Try to parse the key combination
            keyboard.parse_hotkey(key_combination)
            return True
        except Exception as e:
            print(f"Invalid key combination {key_combination}: {e}")
            return False

    @staticmethod
    def normalize_hotkey(key_combination: str) -> str:
        """
        Normalize a key combination to standard format

        Args:
            key_combination: Key combination to normalize

        Returns:
            str: Normalized key combination
        """
        try:
            # Parse and reconstruct to normalize
            parsed = keyboard.parse_hotkey(key_combination)
            return keyboard.get_hotkey_name(parsed)
        except Exception:
            return key_combination

    def wait_for_hotkey_press(self, timeout: Optional[float] = None) -> Optional[str]:
        """
        Wait for user to press a key combination and return it

        Args:
            timeout: Timeout in seconds (None for no timeout)

        Returns:
            str: Key combination pressed or None if timeout
        """
        try:
            event = keyboard.read_event(suppress=True)
            if event.event_type == keyboard.KEY_DOWN:
                return event.name
        except Exception as e:
            print(f"Error reading hotkey: {e}")

        return None
