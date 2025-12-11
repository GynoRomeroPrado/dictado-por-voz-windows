"""
Windows-specific utilities for proper taskbar integration
"""

import sys
import ctypes
from pathlib import Path


def set_app_user_model_id(app_id: str = "GynoRomeroPrado.DictadoPorVoz.1.0"):
    """
    Configura el AppUserModelID para que Windows reconozca
    la aplicación como independiente (no como Python genérico).
    
    Esto permite:
    - Icono correcto en la barra de tareas
    - Notificaciones con el icono personalizado
    - Agrupación correcta de ventanas
    
    Args:
        app_id: Identificador único de la aplicación
    """
    if sys.platform == 'win32':
        try:
            # Cargar shell32.dll
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
            return True
        except Exception as e:
            print(f"Error configurando AppUserModelID: {e}")
            return False
    return False


def get_app_icon_path() -> str:
    """
    Retorna la ruta al icono de la aplicación.
    
    Returns:
        Ruta absoluta al archivo .ico
    """
    # Buscar icono en el directorio de assets
    icon_dir = Path(__file__).parent.parent / "assets"
    icon_path = icon_dir / "app_icon.ico"
    
    if icon_path.exists():
        return str(icon_path)
    
    # Fallback: intentar en directorio raíz
    root_icon = Path(__file__).parent.parent.parent / "app_icon.ico"
    if root_icon.exists():
        return str(root_icon)
    
    return ""
