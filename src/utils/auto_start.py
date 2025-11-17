"""
Utilidades para auto-inicio con Windows
Gestiona la entrada en el registro de Windows para iniciar con el sistema
"""

import os
import sys
import winreg


class AutoStart:
    """Gestiona el auto-inicio de la aplicación con Windows"""

    # Ruta en el registro de Windows para aplicaciones de inicio
    REGISTRY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
    APP_NAME = "DictadoPorVoz"

    @staticmethod
    def get_executable_path():
        """
        Obtiene la ruta del ejecutable actual

        Returns:
            str: Ruta completa del ejecutable
        """
        if getattr(sys, 'frozen', False):
            # Si está ejecutándose como .exe compilado
            return sys.executable
        else:
            # Si está ejecutándose como script Python
            # Retornar el script con python
            script_path = os.path.abspath(sys.argv[0])
            python_path = sys.executable
            return f'"{python_path}" "{script_path}"'

    @staticmethod
    def is_enabled():
        """
        Verifica si el auto-inicio está habilitado

        Returns:
            bool: True si está habilitado, False en caso contrario
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                AutoStart.REGISTRY_PATH,
                0,
                winreg.KEY_READ
            )

            try:
                value, _ = winreg.QueryValueEx(key, AutoStart.APP_NAME)
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False

        except Exception as e:
            print(f"Error verificando auto-inicio: {e}")
            return False

    @staticmethod
    def enable():
        """
        Habilita el auto-inicio con Windows

        Returns:
            bool: True si se habilitó correctamente, False en caso contrario
        """
        try:
            executable_path = AutoStart.get_executable_path()

            # Abrir la clave del registro
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                AutoStart.REGISTRY_PATH,
                0,
                winreg.KEY_SET_VALUE
            )

            # Establecer el valor
            winreg.SetValueEx(
                key,
                AutoStart.APP_NAME,
                0,
                winreg.REG_SZ,
                executable_path
            )

            winreg.CloseKey(key)
            print(f"✓ Auto-inicio habilitado: {executable_path}")
            return True

        except Exception as e:
            print(f"✗ Error habilitando auto-inicio: {e}")
            return False

    @staticmethod
    def disable():
        """
        Deshabilita el auto-inicio con Windows

        Returns:
            bool: True si se deshabilitó correctamente, False en caso contrario
        """
        try:
            # Abrir la clave del registro
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                AutoStart.REGISTRY_PATH,
                0,
                winreg.KEY_SET_VALUE
            )

            # Eliminar el valor
            try:
                winreg.DeleteValue(key, AutoStart.APP_NAME)
                winreg.CloseKey(key)
                print("✓ Auto-inicio deshabilitado")
                return True
            except FileNotFoundError:
                # Ya estaba deshabilitado
                winreg.CloseKey(key)
                return True

        except Exception as e:
            print(f"✗ Error deshabilitando auto-inicio: {e}")
            return False

    @staticmethod
    def toggle():
        """
        Alterna el estado del auto-inicio

        Returns:
            bool: Nuevo estado (True = habilitado, False = deshabilitado)
        """
        if AutoStart.is_enabled():
            AutoStart.disable()
            return False
        else:
            AutoStart.enable()
            return True
