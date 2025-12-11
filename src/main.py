"""
Dictado por Voz - Punto de entrada principal
Aplicación de dictado por voz universal para Windows usando Whisper

Uso:
    python -m src.main
    
    o con Poetry:
    poetry run python -m src.main
"""

import sys
import logging
import os
import tempfile
import atexit
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Archivo de bloqueo para instancia única (guarda el PID)
LOCK_FILE = Path(tempfile.gettempdir()) / "dictado_por_voz.lock"


def kill_previous_instance():
    """
    Busca y termina cualquier instancia anterior de la aplicación.
    Usa el archivo de bloqueo que contiene el PID de la instancia anterior.
    """
    import signal
    
    if LOCK_FILE.exists():
        try:
            pid = int(LOCK_FILE.read_text().strip())
            logger.info(f"Encontrada instancia anterior con PID {pid}, terminándola...")
            
            # Intentar terminar el proceso
            try:
                os.kill(pid, signal.SIGTERM)
                import time
                time.sleep(0.5)  # Dar tiempo para limpieza
            except (ProcessLookupError, PermissionError):
                # El proceso ya no existe
                pass
            except Exception as e:
                logger.debug(f"Error terminando proceso {pid}: {e}")
            
            # Eliminar archivo de bloqueo
            LOCK_FILE.unlink(missing_ok=True)
            logger.info("Instancia anterior terminada")
            
        except (ValueError, FileNotFoundError):
            # Archivo corrupto o no existe
            LOCK_FILE.unlink(missing_ok=True)
        except Exception as e:
            logger.debug(f"Error procesando lock file: {e}")


def check_single_instance():
    """
    Asegura que solo una instancia de la aplicación se ejecute.
    Si hay una instancia anterior, la cierra automáticamente.
    
    Returns:
        True siempre (cierra instancias anteriores)
    """
    # Primero, terminar cualquier instancia anterior
    kill_previous_instance()
    
    # Guardar nuestro PID en el archivo de bloqueo
    try:
        LOCK_FILE.write_text(str(os.getpid()))
        logger.info(f"Instancia registrada con PID {os.getpid()}")
    except Exception as e:
        logger.warning(f"No se pudo crear archivo de bloqueo: {e}")
    
    return True


def cleanup_lock_file():
    """Limpia el archivo de bloqueo al cerrar la aplicación"""
    try:
        if LOCK_FILE.exists():
            # Solo eliminar si el PID coincide
            try:
                stored_pid = int(LOCK_FILE.read_text().strip())
                if stored_pid == os.getpid():
                    LOCK_FILE.unlink(missing_ok=True)
            except Exception:
                pass
    except Exception:
        pass


def setup_theme(app):
    """Configura el tema oscuro de la aplicación"""
    try:
        import qdarktheme
        from .utils.config import config
        
        theme = config.get('ui.theme', 'auto')
        qdarktheme.setup_theme(theme)
        logger.info(f"Tema configurado: {theme}")
    except ImportError:
        logger.warning("qdarktheme no disponible, usando tema por defecto")
    except Exception as e:
        logger.warning(f"Error configurando tema: {e}")


def main():
    """Función principal de la aplicación"""
    
    # Cerrar instancia anterior si existe y registrar esta nueva
    check_single_instance()
    
    # Registrar limpieza al salir
    atexit.register(cleanup_lock_file)
    
    logger.info("Iniciando Dictado por Voz...")
    
    # Crear aplicación Qt
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import Qt
    
    # Habilitar modo oscuro nativo en Windows
    if sys.platform == 'win32':
        sys.argv += ['-platform', 'windows:darkmode=2']
    
    app = QApplication(sys.argv)
    app.setApplicationName("Dictado por Voz")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("GynoRomeroPrado")
    
    # Configurar tema
    setup_theme(app)
    
    # No cerrar la app cuando se cierra la ventana principal
    app.setQuitOnLastWindowClosed(False)
    
    # Importar componentes
    from .utils.config import config
    from .core.hotkey_manager import HotkeyManager
    from .core.command_processor import CommandProcessor
    from .core.speech_recognizer import SpeechRecognizer  # Whisper optimizado
    from .ui.main_window import MainWindow
    from .ui.settings_dialog import SettingsDialog
    from .ui.system_tray import SystemTrayIcon
    from .ui.floating_widget import FloatingWidgetManager
    
    # Crear componentes
    logger.info("Inicializando componentes...")
    
    recognizer = SpeechRecognizer()  # Whisper con puntuación automática
    processor = CommandProcessor()
    hotkeys = HotkeyManager()
    
    # Crear UI
    main_window = MainWindow()
    settings_dialog = SettingsDialog(main_window)
    tray_icon = SystemTrayIcon()
    floating_widgets = FloatingWidgetManager()
    
    # ===== Conectar señales =====
    
    # Recognizer -> Window
    recognizer.listening_started.connect(lambda: main_window.set_listening_state(True))
    recognizer.listening_stopped.connect(lambda: main_window.set_listening_state(False))
    recognizer.error_occurred.connect(main_window.show_error)
    
    # Recognizer -> Tray
    recognizer.listening_started.connect(lambda: tray_icon.set_listening_state(True))
    recognizer.listening_stopped.connect(lambda: tray_icon.set_listening_state(False))
    
    # Recognizer -> Floating Widget
    recognizer.listening_started.connect(lambda: floating_widgets.set_listening_state(True))
    recognizer.listening_stopped.connect(lambda: floating_widgets.set_listening_state(False))
    
    # Recognizer -> Processor -> Salida
    def on_text_recognized(text: str):
        """Procesa texto reconocido por Whisper (con puntuación automática)"""
        processed_text, is_action = processor.process_text(text)
        
        if is_action:
            # Es un comando de acción
            if "stop" in text.lower() or "detener" in text.lower():
                recognizer.stop_listening()
        elif processed_text:
            # Es texto normal o puntuación - insertar
            processor.add_to_buffer(processed_text)
            main_window.append_text(processed_text)
            floating_widgets.show_recognized_text(processed_text)  # Mostrar en overlay
            processor.insert_text(processed_text)
    
    recognizer.text_recognized.connect(on_text_recognized)
    
    # ===== Callbacks de UI =====
    
    def toggle_dictation():
        """Alterna el estado de dictado"""
        is_listening = recognizer.toggle_listening()
        if is_listening:
            tray_icon.show_notification(
                "Dictado activado",
                "Habla ahora para dictar texto",
                duration=2000
            )
        else:
            tray_icon.show_notification(
                "Dictado detenido",
                "Dictado pausado",
                duration=2000
            )
    
    def stop_dictation():
        """Detiene el dictado"""
        if recognizer.is_listening:
            recognizer.stop_listening()
    
    def open_settings():
        """Abre el diálogo de configuración"""
        if recognizer.is_listening:
            recognizer.stop_listening()
        settings_dialog.exec()
    
    def on_settings_changed():
        """Callback cuando cambia la configuración"""
        # Recargar comandos
        processor.reload_commands()
        
        # Actualizar hotkeys
        hotkeys.unregister_all()
        hotkeys.register_default_hotkeys(
            toggle_dictation,
            stop_dictation,
            open_settings
        )
        
        logger.info("Configuración actualizada")
    
    def exit_app():
        """Cierra la aplicación"""
        logger.info("Cerrando aplicación...")
        recognizer.stop_listening()
        hotkeys.unregister_all()
        tray_icon.hide()
        app.quit()
    
    def show_main_window():
        """Muestra la ventana principal"""
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()
    
    def on_close_to_tray():
        """Callback cuando se minimiza a la bandeja"""
        tray_icon.show_notification(
            "Dictado por Voz",
            "La aplicación sigue ejecutándose en segundo plano",
            duration=2000
        )
    
    # Asignar callbacks a la ventana
    main_window.on_toggle_dictation = toggle_dictation
    main_window.on_stop_dictation = stop_dictation
    main_window.on_open_settings = open_settings
    main_window.on_clear_history = processor.clear_buffer
    main_window.on_close_to_tray = on_close_to_tray
    
    # Conectar señales del tray
    tray_icon.toggle_requested.connect(toggle_dictation)
    tray_icon.show_window_requested.connect(show_main_window)
    tray_icon.settings_requested.connect(open_settings)
    tray_icon.exit_requested.connect(exit_app)
    
    # Conectar botón flotante
    floating_widgets.on_toggle_dictation = toggle_dictation
    
    # Conectar señales del diálogo de configuración
    settings_dialog.settings_changed.connect(on_settings_changed)
    
    # ===== Registrar hotkeys =====
    logger.info("Registrando hotkeys globales...")
    hotkeys.register_default_hotkeys(
        toggle_dictation,
        stop_dictation,
        open_settings
    )
    
    # ===== Mostrar UI =====
    if not config.get('ui.start_minimized', False):
        main_window.show()
    
    # Mostrar botón flotante siempre
    floating_widgets.show()
    
    # Mostrar notificación de inicio
    tray_icon.show_notification(
        "Dictado por Voz iniciado",
        f"Presiona {config.get('hotkeys.toggle_dictation', 'Ctrl+Shift+Space')} para dictar",
        duration=3000
    )
    
    logger.info("Aplicación iniciada correctamente")
    logger.info(f"Hotkey de activación: {config.get('hotkeys.toggle_dictation', 'Ctrl+Shift+Space')}")
    
    # Ejecutar event loop
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
