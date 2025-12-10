"""
ConfigManager - Gestión de configuración para Dictado por Voz
Maneja settings.json y commands.json con persistencia automática
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


class ConfigManager:
    """
    Gestor de configuración singleton.
    Carga y guarda configuraciones desde archivos JSON.
    Soporta notación de punto para acceso a valores anidados.
    """
    
    _instance: Optional['ConfigManager'] = None
    
    def __new__(cls) -> 'ConfigManager':
        """Implementación del patrón Singleton"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Inicializa el ConfigManager si no está ya inicializado"""
        if self._initialized:
            return
            
        # Determinar directorio base (compatible con PyInstaller)
        if getattr(os.sys, 'frozen', False):
            self.base_dir = Path(os.sys.executable).parent
        else:
            self.base_dir = Path(__file__).parent.parent.parent
        
        self.config_dir = self.base_dir / 'config'
        self.settings_file = self.config_dir / 'settings.json'
        self.commands_file = self.config_dir / 'commands.json'
        
        self.settings: Dict[str, Any] = {}
        self.commands: Dict[str, Any] = {}
        
        self.load_config()
        self._initialized = True
    
    def load_config(self) -> None:
        """Carga la configuración desde los archivos JSON"""
        # Crear directorio config si no existe
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Cargar settings
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.settings = self._get_default_settings()
        else:
            self.settings = self._get_default_settings()
            self.save_settings()
        
        # Cargar commands
        if self.commands_file.exists():
            try:
                with open(self.commands_file, 'r', encoding='utf-8') as f:
                    self.commands = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.commands = self._get_default_commands()
        else:
            self.commands = self._get_default_commands()
            self.save_commands()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor de configuración usando notación de punto.
        Ejemplo: config.get('recognition.engine') -> 'whisper_local'
        """
        keys = key.split('.')
        value = self.settings
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any, save: bool = True) -> None:
        """
        Establece un valor de configuración usando notación de punto.
        Crea estructuras anidadas automáticamente si no existen.
        """
        keys = key.split('.')
        current = self.settings
        
        # Navegar/crear estructura hasta el penúltimo nivel
        for k in keys[:-1]:
            if k not in current or not isinstance(current[k], dict):
                current[k] = {}
            current = current[k]
        
        # Establecer el valor
        current[keys[-1]] = value
        
        if save:
            self.save_settings()
    
    def save_settings(self) -> bool:
        """Guarda la configuración de settings en disco"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False
    
    def save_commands(self) -> bool:
        """Guarda la configuración de commands en disco"""
        try:
            with open(self.commands_file, 'w', encoding='utf-8') as f:
                json.dump(self.commands, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False
    
    def save_config(self) -> bool:
        """Guarda toda la configuración"""
        return self.save_settings() and self.save_commands()
    
    def get_command(self, command_type: str) -> Dict[str, Any]:
        """Obtiene comandos de un tipo específico"""
        return self.commands.get(command_type, {})
    
    def get_all_commands(self) -> Dict[str, Any]:
        """Obtiene todos los comandos"""
        return self.commands
    
    def add_custom_command(self, command: Dict[str, Any]) -> bool:
        """Añade un comando personalizado"""
        if 'custom_commands' not in self.commands:
            self.commands['custom_commands'] = []
        
        self.commands['custom_commands'].append(command)
        return self.save_commands()
    
    def remove_custom_command(self, command_id: str) -> bool:
        """Elimina un comando personalizado por su ID"""
        if 'custom_commands' not in self.commands:
            return False
        
        original_len = len(self.commands['custom_commands'])
        self.commands['custom_commands'] = [
            cmd for cmd in self.commands['custom_commands']
            if cmd.get('id') != command_id
        ]
        
        if len(self.commands['custom_commands']) < original_len:
            return self.save_commands()
        return False
    
    def update_custom_command(self, command_id: str, updated: Dict[str, Any]) -> bool:
        """Actualiza un comando personalizado existente"""
        if 'custom_commands' not in self.commands:
            return False
        
        for i, cmd in enumerate(self.commands['custom_commands']):
            if cmd.get('id') == command_id:
                self.commands['custom_commands'][i] = updated
                return self.save_commands()
        return False
    
    def _get_default_settings(self) -> Dict[str, Any]:
        """Retorna la configuración por defecto"""
        return {
            "version": "1.0.0",
            "language": "es-PE",
            "recognition": {
                "engine": "whisper_local",
                "model": "medium",
                "confidence_threshold": 0.7,
                "energy_threshold": 600,
                "dynamic_energy": True,
                "pause_threshold": 0.8
            },
            "hotkeys": {
                "toggle_dictation": "ctrl+shift+space",
                "stop_dictation": "ctrl+shift+s",
                "open_settings": "ctrl+shift+o"
            },
            "output": {
                "auto_insert": True,
                "use_clipboard": False,
                "paste_delay": 0.1,
                "auto_copy": True
            },
            "ui": {
                "show_main_window": True,
                "minimize_to_tray": True,
                "always_on_top": False,
                "start_minimized": False,
                "show_notifications": True,
                "theme": "auto"
            },
            "advanced": {
                "auto_punctuation": True,
                "auto_capitalization": True,
                "enable_custom_commands": True,
                "save_transcriptions": False
            },
            "audio": {
                "feedback_enabled": True,
                "beep_on_start": True,
                "beep_on_stop": True
            }
        }
    
    def _get_default_commands(self) -> Dict[str, Any]:
        """Retorna los comandos por defecto"""
        return {
            "punctuation_commands": {
                "punto": ".",
                "coma": ",",
                "dos puntos": ":",
                "punto y coma": ";",
                "signo de interrogación": "?",
                "interrogación": "?",
                "signo de exclamación": "!",
                "exclamación": "!",
                "abrir paréntesis": "(",
                "cerrar paréntesis": ")",
                "abrir comillas": "\"",
                "cerrar comillas": "\"",
                "guión": "-",
                "guion": "-",
                "barra": "/",
                "arroba": "@",
                # Comandos en inglés
                "period": ".",
                "comma": ",",
                "colon": ":",
                "semicolon": ";",
                "question mark": "?",
                "exclamation mark": "!",
                "open parenthesis": "(",
                "close parenthesis": ")",
                "hyphen": "-",
                "slash": "/",
                "at sign": "@"
            },
            "formatting_commands": {
                "nueva línea": "\n",
                "nuevo párrafo": "\n\n",
                "tabulador": "\t",
                "tabulación": "\t",
                "new line": "\n",
                "new paragraph": "\n\n",
                "tab": "\t"
            },
            "action_commands": {
                "borrar todo": {"action": "clear_buffer"},
                "clear all": {"action": "clear_buffer"},
                "borrar última palabra": {"action": "delete_last_word", "params": 1},
                "delete last word": {"action": "delete_last_word", "params": 1},
                "detener dictado": {"action": "stop_dictation"},
                "stop dictation": {"action": "stop_dictation"}
            },
            "custom_commands": []
        }


# Instancia singleton global
config = ConfigManager()
