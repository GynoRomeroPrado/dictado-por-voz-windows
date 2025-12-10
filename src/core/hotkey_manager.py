"""
HotkeyManager - Gestión de atajos de teclado globales
Permite registrar hotkeys que funcionan en cualquier aplicación de Windows
"""

import logging
from typing import Callable, Dict, Optional, Set

try:
    import keyboard
except ImportError:
    keyboard = None

from ..utils.config import config

logger = logging.getLogger(__name__)


class HotkeyManager:
    """
    Gestor de hotkeys globales.
    Registra y gestiona atajos de teclado que funcionan en todo el sistema.
    """
    
    def __init__(self):
        """Inicializa el HotkeyManager cargando configuración de hotkeys"""
        self.registered_keys: Set[str] = set()
        self._callbacks: Dict[str, Callable] = {}
        
        # Cargar hotkeys desde configuración
        self.toggle_dictation_key = config.get('hotkeys.toggle_dictation', 'ctrl+shift+space')
        self.stop_dictation_key = config.get('hotkeys.stop_dictation', 'ctrl+shift+s')
        self.open_settings_key = config.get('hotkeys.open_settings', 'ctrl+shift+o')
    
    def register_hotkey(self, combo: str, callback: Callable, description: str = "") -> bool:
        """
        Registra un hotkey global.
        
        Args:
            combo: Combinación de teclas (ej: 'ctrl+shift+space')
            callback: Función a ejecutar cuando se presiona el hotkey
            description: Descripción opcional del hotkey
            
        Returns:
            True si el registro fue exitoso
        """
        if keyboard is None:
            logger.error("Módulo keyboard no disponible")
            return False
        
        try:
            keyboard.add_hotkey(combo, callback, suppress=False)
            self.registered_keys.add(combo)
            self._callbacks[combo] = callback
            logger.info(f"Hotkey registrado: {combo} - {description}")
            return True
        except Exception as e:
            logger.error(f"Error registrando hotkey {combo}: {e}")
            return False
    
    def unregister_hotkey(self, combo: str) -> bool:
        """
        Desregistra un hotkey.
        
        Args:
            combo: Combinación de teclas a desregistrar
            
        Returns:
            True si se desregistró correctamente
        """
        if keyboard is None:
            return False
        
        try:
            keyboard.remove_hotkey(combo)
            self.registered_keys.discard(combo)
            self._callbacks.pop(combo, None)
            logger.info(f"Hotkey desregistrado: {combo}")
            return True
        except Exception as e:
            logger.error(f"Error desregistrando hotkey {combo}: {e}")
            return False
    
    def unregister_all(self) -> None:
        """Desregistra todos los hotkeys"""
        if keyboard is None:
            return
        
        for combo in list(self.registered_keys):
            try:
                keyboard.remove_hotkey(combo)
            except Exception:
                pass
        
        self.registered_keys.clear()
        self._callbacks.clear()
        logger.info("Todos los hotkeys desregistrados")
    
    def register_default_hotkeys(
        self,
        toggle_callback: Callable,
        stop_callback: Callable,
        settings_callback: Callable
    ) -> None:
        """
        Registra los hotkeys predeterminados de la aplicación.
        
        Args:
            toggle_callback: Callback para activar/desactivar dictado
            stop_callback: Callback para detener dictado
            settings_callback: Callback para abrir configuración
        """
        self.register_hotkey(
            self.toggle_dictation_key,
            toggle_callback,
            "Activar/desactivar dictado"
        )
        self.register_hotkey(
            self.stop_dictation_key,
            stop_callback,
            "Detener dictado"
        )
        self.register_hotkey(
            self.open_settings_key,
            settings_callback,
            "Abrir configuración"
        )
    
    def update_hotkey(self, name: str, new_combo: str, callback: Callable) -> bool:
        """
        Actualiza un hotkey con una nueva combinación.
        
        Args:
            name: Nombre del hotkey ('toggle_dictation', 'stop_dictation', etc.)
            new_combo: Nueva combinación de teclas
            callback: Callback asociado
            
        Returns:
            True si la actualización fue exitosa
        """
        # Obtener la combinación actual
        current_combo = getattr(self, f"{name}_key", None)
        
        if current_combo and current_combo in self.registered_keys:
            self.unregister_hotkey(current_combo)
        
        # Registrar nuevo hotkey
        success = self.register_hotkey(new_combo, callback, name)
        
        if success:
            setattr(self, f"{name}_key", new_combo)
            config.set(f'hotkeys.{name}', new_combo)
        
        return success
    
    def is_hotkey_available(self, combo: str) -> bool:
        """
        Verifica si una combinación de teclas está disponible.
        
        Args:
            combo: Combinación de teclas a verificar
            
        Returns:
            True si la combinación no está registrada
        """
        return combo not in self.registered_keys
    
    def test_hotkey(self, combo: str) -> bool:
        """
        Prueba si una combinación de teclas es válida.
        
        Args:
            combo: Combinación de teclas a probar
            
        Returns:
            True si la combinación es válida
        """
        if keyboard is None:
            return False
        
        try:
            keyboard.parse_hotkey(combo)
            return True
        except Exception:
            return False
    
    def normalize_hotkey(self, combo: str) -> str:
        """
        Normaliza el formato de una combinación de teclas.
        
        Args:
            combo: Combinación de teclas a normalizar
            
        Returns:
            Combinación normalizada en minúsculas
        """
        if keyboard is None:
            return combo.lower().replace(' ', '')
        
        try:
            keyboard.parse_hotkey(combo)
            # Normalizar formato
            normalized = combo.lower().replace(' ', '')
            return normalized
        except Exception:
            return combo.lower().replace(' ', '')
    
    def get_registered_hotkeys(self) -> Dict[str, str]:
        """
        Obtiene un diccionario con los hotkeys registrados.
        
        Returns:
            Dict con nombres y combinaciones de hotkeys
        """
        return {
            'toggle_dictation': self.toggle_dictation_key,
            'stop_dictation': self.stop_dictation_key,
            'open_settings': self.open_settings_key
        }
