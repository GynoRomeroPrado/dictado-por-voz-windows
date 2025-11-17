# Ejemplos de Uso

Este directorio contiene ejemplos de cómo usar los componentes del proyecto programáticamente.

## Archivos

### `api_usage.py`

Ejemplos completos de cómo usar cada componente de la API:

1. **ConfigManager**: Gestión de configuración
2. **ClipboardManager**: Operaciones de portapapeles
3. **SpeechRecognizer**: Reconocimiento de voz
4. **CommandProcessor**: Procesamiento de comandos
5. **HotkeyManager**: Gestión de hotkeys globales
6. **Complete Workflow**: Flujo completo de trabajo
7. **Custom Command Handler**: Handler personalizado de comandos

## Ejecutar Ejemplos

```bash
# Asegúrate de estar en el directorio raíz del proyecto
cd dictado-por-voz-windows

# Ejecuta los ejemplos
python examples/api_usage.py
```

## Requisitos

Para ejecutar los ejemplos, necesitas tener instaladas las dependencias:

```bash
pip install -r requirements.txt
```

**Nota**: Algunos ejemplos requieren permisos de administrador en Windows (especialmente los relacionados con hotkeys globales).

## Usar en Tu Proyecto

Puedes copiar estos ejemplos y adaptarlos a tus necesidades. Los componentes están diseñados para ser usados de forma independiente:

```python
# Importar solo lo que necesitas
from src.utils.config import ConfigManager
from src.core.command_processor import CommandProcessor

# Usar los componentes
config = ConfigManager()
processor = CommandProcessor()
```

## Documentación

Para documentación completa de la API, consulta los docstrings en el código fuente:

- `src/utils/config.py`
- `src/utils/clipboard.py`
- `src/core/speech_recognizer.py`
- `src/core/command_processor.py`
- `src/core/hotkey_manager.py`
