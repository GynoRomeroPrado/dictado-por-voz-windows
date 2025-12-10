"""
CommandProcessor - Procesamiento de comandos de voz
Convierte texto reconocido en comandos y texto formateado
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from ..utils.config import config
from ..utils.clipboard import ClipboardManager

logger = logging.getLogger(__name__)


class CommandProcessor:
    """
    Procesa texto reconocido, detectando comandos de puntuación,
    formato y acciones personalizadas.
    """
    
    def __init__(self):
        """Inicializa el CommandProcessor cargando comandos desde config"""
        self.text_buffer: List[str] = []
        self.clipboard = ClipboardManager()
        
        # Cargar configuración
        self.auto_punctuation = config.get('advanced.auto_punctuation', True)
        self.auto_capitalization = config.get('advanced.auto_capitalization', True)
        self.enable_custom_commands = config.get('advanced.enable_custom_commands', True)
        
        # Cargar comandos
        self.reload_commands()
    
    def reload_commands(self) -> None:
        """Recarga los comandos desde la configuración"""
        self.commands = config.get_all_commands()
        self.punctuation_commands = self.commands.get('punctuation_commands', {})
        self.formatting_commands = self.commands.get('formatting_commands', {})
        self.action_commands = self.commands.get('action_commands', {})
        self.custom_commands = self.commands.get('custom_commands', [])
        logger.info("Comandos recargados desde configuración")
    
    def process_text(self, text: str) -> Tuple[Optional[str], bool]:
        """
        Procesa texto reconocido, detectando comandos.
        
        Args:
            text: Texto a procesar
            
        Returns:
            Tupla (texto_procesado, es_accion)
            - texto_procesado: Texto resultante o None si es acción
            - es_accion: True si el texto era un comando de acción
        """
        if not text or not text.strip():
            return None, False
        
        text = text.strip()
        text_lower = text.lower()
        
        # 1. Verificar comandos de puntuación
        if text_lower in self.punctuation_commands:
            return self.punctuation_commands[text_lower], False
        
        # 2. Verificar comandos de formato
        if text_lower in self.formatting_commands:
            return self.formatting_commands[text_lower], False
        
        # 3. Verificar comandos de acción
        if text_lower in self.action_commands:
            self._execute_action_command(text_lower)
            return None, True
        
        # 4. Verificar comandos personalizados
        if self.enable_custom_commands:
            for cmd in self.custom_commands:
                if not cmd.get('enabled', True):
                    continue
                    
                trigger = cmd.get('trigger', '').lower()
                if text_lower == trigger:
                    result = self._execute_custom_command(cmd)
                    if result is not None:
                        return result, False
                    return None, True
        
        # 5. Texto normal - aplicar formato
        processed = self._format_text(text)
        return processed, False
    
    def _format_text(self, text: str) -> str:
        """
        Aplica formato automático al texto (capitalización, espaciado).
        
        Args:
            text: Texto a formatear
            
        Returns:
            Texto formateado
        """
        if not self.auto_capitalization:
            return text
        
        # Capitalizar primera letra si es inicio de oración
        if self._should_capitalize():
            text = text[0].upper() + text[1:] if len(text) > 1 else text.upper()
        
        return text
    
    def _should_capitalize(self) -> bool:
        """
        Determina si el siguiente texto debe empezar con mayúscula.
        
        Returns:
            True si debe capitalizarse
        """
        if not self.text_buffer:
            return True
        
        # Obtener último texto del buffer
        last_text = self.get_buffer_text()
        if not last_text:
            return True
        
        # Capitalizar después de . ? ! y nueva línea
        last_char = last_text.rstrip()[-1] if last_text.rstrip() else ''
        return last_char in '.?!\n'
    
    def _execute_action_command(self, command_key: str) -> None:
        """
        Ejecuta un comando de acción.
        
        Args:
            command_key: Clave del comando a ejecutar
        """
        command = self.action_commands.get(command_key, {})
        action = command.get('action', '') if isinstance(command, dict) else command
        
        if action == 'clear_buffer':
            self.clear_buffer()
            logger.info("Buffer limpiado")
        elif action == 'delete_last_word':
            self._delete_last_word()
            logger.info("Última palabra borrada")
        elif action == 'stop_dictation':
            # Esta acción será manejada por el SpeechRecognizer
            logger.info("Comando: detener dictado")
    
    def _delete_last_word(self) -> None:
        """Borra la última palabra del buffer y de la aplicación activa"""
        if self.text_buffer:
            last_text = self.text_buffer[-1]
            # Contar caracteres de la última palabra
            words = last_text.split()
            if words:
                last_word_len = len(words[-1]) + 1  # +1 para el espacio
                self.clipboard.delete_characters(last_word_len)
                
                # Actualizar buffer
                remaining = ' '.join(words[:-1])
                if remaining:
                    self.text_buffer[-1] = remaining
                else:
                    self.text_buffer.pop()
    
    def _execute_custom_command(self, command: Dict[str, Any]) -> Optional[str]:
        """
        Ejecuta un comando personalizado.
        
        Args:
            command: Diccionario con la definición del comando
            
        Returns:
            Texto a insertar o None si es una acción
        """
        action = command.get('action', '')
        
        if action == 'insert_text':
            return command.get('value', '')
        
        elif action == 'insert_date':
            date_format = command.get('format', '%d/%m/%Y')
            try:
                return datetime.now().strftime(date_format)
            except Exception:
                return datetime.now().strftime('%d/%m/%Y')
        
        elif action == 'open_url':
            import webbrowser
            url = command.get('value', '')
            if url:
                webbrowser.open(url)
            return None
        
        return None
    
    def add_to_buffer(self, text: str) -> None:
        """
        Añade texto al buffer interno.
        
        Args:
            text: Texto a añadir
        """
        self.text_buffer.append(text)
    
    def clear_buffer(self) -> None:
        """Limpia el buffer de texto"""
        self.text_buffer.clear()
    
    def get_buffer_text(self) -> str:
        """
        Obtiene todo el texto del buffer concatenado.
        
        Returns:
            Texto completo del buffer
        """
        return ''.join(self.text_buffer)
    
    def insert_text(self, text: str) -> bool:
        """
        Inserta texto en la aplicación activa.
        
        Args:
            text: Texto a insertar
            
        Returns:
            True si la inserción fue exitosa
        """
        use_clipboard = config.get('output.use_clipboard', False)
        auto_insert = config.get('output.auto_insert', True)
        
        if not auto_insert:
            # Solo copiar al portapapeles
            return self.clipboard.copy_to_clipboard(text)
        
        if use_clipboard:
            # Insertar via Ctrl+V
            delay = config.get('output.paste_delay', 0.1)
            return self.clipboard.insert_text(text, delay=delay)
        else:
            # Escribir carácter por carácter
            return self.clipboard.type_text(text)
