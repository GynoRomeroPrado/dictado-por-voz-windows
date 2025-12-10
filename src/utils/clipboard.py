"""
ClipboardManager - Gestión de portapapeles e inserción de texto
Maneja la inserción de texto en la aplicación activa de Windows
"""

import time
from typing import Optional

try:
    import pyperclip
except ImportError:
    pyperclip = None

try:
    import keyboard
except ImportError:
    keyboard = None


class ClipboardManager:
    """
    Gestiona operaciones del portapapeles e inserción de texto.
    Todos los métodos son estáticos para facilitar el uso.
    """
    
    @staticmethod
    def copy_to_clipboard(text: str) -> bool:
        """
        Copia texto al portapapeles.
        
        Args:
            text: Texto a copiar
            
        Returns:
            True si la operación fue exitosa
        """
        if pyperclip is None:
            return False
            
        try:
            pyperclip.copy(text)
            return True
        except Exception:
            return False
    
    @staticmethod
    def paste_from_clipboard() -> str:
        """
        Obtiene texto del portapapeles.
        
        Returns:
            Contenido del portapapeles o cadena vacía si hay error
        """
        if pyperclip is None:
            return ""
            
        try:
            return pyperclip.paste()
        except Exception:
            return ""
    
    @staticmethod
    def insert_text(text: str, delay: float = 0.1) -> bool:
        """
        Inserta texto en la aplicación activa usando Ctrl+V.
        Preserva el contenido original del portapapeles.
        
        Args:
            text: Texto a insertar
            delay: Retardo antes de pegar (segundos)
            
        Returns:
            True si la operación fue exitosa
        """
        if pyperclip is None or keyboard is None:
            return False
            
        try:
            # Guardar contenido original del portapapeles
            original_clipboard = pyperclip.paste()
            
            # Copiar nuevo texto
            pyperclip.copy(text)
            
            # Pequeño delay para asegurar que el portapapeles se actualice
            time.sleep(delay)
            
            # Simular Ctrl+V
            keyboard.send('ctrl+v')
            
            # Esperar a que se complete el pegado
            time.sleep(0.05)
            
            # Restaurar portapapeles original
            pyperclip.copy(original_clipboard)
            
            return True
        except Exception:
            return False
    
    @staticmethod
    def type_text(text: str, delay: float = 0.01) -> bool:
        """
        Escribe texto carácter por carácter.
        Más lento pero más compatible con algunas aplicaciones.
        
        Args:
            text: Texto a escribir
            delay: Retardo entre caracteres (segundos)
            
        Returns:
            True si la operación fue exitosa
        """
        if keyboard is None:
            return False
            
        try:
            keyboard.write(text, delay=delay)
            return True
        except Exception:
            return False
    
    @staticmethod
    def simulate_keypress(keys: str) -> bool:
        """
        Simula una combinación de teclas.
        
        Args:
            keys: Combinación de teclas (ej: 'ctrl+enter')
            
        Returns:
            True si la operación fue exitosa
        """
        if keyboard is None:
            return False
            
        try:
            keyboard.send(keys)
            return True
        except Exception:
            return False
    
    @staticmethod
    def delete_characters(count: int, delay: float = 0.01) -> bool:
        """
        Borra N caracteres usando la tecla Backspace.
        
        Args:
            count: Número de caracteres a borrar
            delay: Retardo entre pulsaciones
            
        Returns:
            True si la operación fue exitosa
        """
        if keyboard is None:
            return False
            
        try:
            for _ in range(count):
                keyboard.send('backspace')
                time.sleep(delay)
            return True
        except Exception:
            return False
    
    @staticmethod
    def delete_last_word() -> bool:
        """
        Borra la última palabra usando Ctrl+Backspace.
        
        Returns:
            True si la operación fue exitosa
        """
        if keyboard is None:
            return False
            
        try:
            keyboard.send('ctrl+backspace')
            return True
        except Exception:
            return False
