# Guía de Contribución

¡Gracias por tu interés en contribuir a Dictado por Voz - Windows! Este documento te guiará en el proceso.

## Código de Conducta

- Sé respetuoso y constructivo
- Acepta críticas constructivas
- Enfócate en lo mejor para la comunidad
- Muestra empatía hacia otros miembros

## ¿Cómo Puedo Contribuir?

### Reportar Bugs

Si encuentras un bug, por favor crea un issue incluyendo:

1. **Título descriptivo**
2. **Pasos para reproducir** el problema
3. **Comportamiento esperado** vs. **comportamiento actual**
4. **Versión** de Python y del sistema operativo
5. **Logs** o capturas de pantalla si es posible

**Plantilla de Bug Report:**
```markdown
### Descripción
[Descripción breve del problema]

### Pasos para Reproducir
1. [Primer paso]
2. [Segundo paso]
3. [...]

### Comportamiento Esperado
[Qué debería pasar]

### Comportamiento Actual
[Qué está pasando]

### Entorno
- OS: Windows 10/11
- Python: 3.x
- Versión de la app: x.x.x

### Logs
```
[Pega logs relevantes aquí]
```
```

### Sugerir Mejoras

Las sugerencias de nuevas características son bienvenidas. Incluye:

1. **Caso de uso**: Por qué es útil esta característica
2. **Propuesta**: Cómo funcionaría
3. **Alternativas**: Otras formas de lograr lo mismo

### Contribuir con Código

#### Configuración del Entorno de Desarrollo

1. Fork el repositorio
2. Clona tu fork:
   ```bash
   git clone https://github.com/TU_USUARIO/dictado-por-voz-windows.git
   ```
3. Crea un entorno virtual:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
4. Instala dependencias de desarrollo:
   ```bash
   pip install -r requirements.txt
   pip install pytest black flake8 mypy
   ```

#### Proceso de Desarrollo

1. **Crea una rama** para tu feature:
   ```bash
   git checkout -b feature/nombre-descriptivo
   ```

2. **Haz tus cambios** siguiendo las guías de estilo

3. **Escribe tests** si es aplicable

4. **Ejecuta los tests**:
   ```bash
   pytest tests/
   ```

5. **Formatea el código**:
   ```bash
   black src/
   ```

6. **Verifica estilo**:
   ```bash
   flake8 src/
   ```

7. **Commit** tus cambios:
   ```bash
   git add .
   git commit -m "feat: descripción breve del cambio"
   ```

8. **Push** a tu fork:
   ```bash
   git push origin feature/nombre-descriptivo
   ```

9. **Abre un Pull Request** en GitHub

#### Convenciones de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva característica
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Formateo, punto y coma faltantes, etc.
- `refactor:` Refactorización de código
- `test:` Añadir o corregir tests
- `chore:` Tareas de mantenimiento

Ejemplos:
```
feat: añadir soporte para comandos de voz personalizados
fix: corregir error al iniciar micrófono en Windows 11
docs: actualizar README con instrucciones de instalación
```

### Guías de Estilo

#### Python

- Seguimos [PEP 8](https://pep8.org/)
- Usa `black` para formateo automático
- Máximo 100 caracteres por línea
- Usa type hints cuando sea posible

**Ejemplo:**
```python
def process_text(text: str, options: Dict[str, Any]) -> Optional[str]:
    """
    Procesa el texto reconocido.

    Args:
        text: Texto a procesar
        options: Opciones de procesamiento

    Returns:
        Texto procesado o None si falla
    """
    if not text:
        return None

    # Implementación...
    return processed_text
```

#### Docstrings

Usamos estilo Google:
```python
def function(arg1: int, arg2: str) -> bool:
    """
    Descripción breve de una línea.

    Descripción detallada si es necesaria.

    Args:
        arg1: Descripción del argumento 1
        arg2: Descripción del argumento 2

    Returns:
        Descripción del valor de retorno

    Raises:
        ValueError: Si arg1 es negativo
    """
    pass
```

#### Organización de Imports

```python
# 1. Librería estándar
import os
import sys
from typing import Optional

# 2. Librerías de terceros
import speech_recognition as sr
from PyQt5.QtWidgets import QWidget

# 3. Imports locales
from ..utils.config import config
from .command_processor import CommandProcessor
```

### Áreas que Necesitan Ayuda

Siempre buscamos ayuda en:

- 📝 **Documentación**: Mejorar guías y tutoriales
- 🌍 **Internacionalización**: Traducir a otros idiomas
- 🐛 **Corrección de bugs**: Ver issues etiquetados como "bug"
- ✨ **Nuevas características**: Ver issues etiquetados como "enhancement"
- 🧪 **Tests**: Aumentar cobertura de tests
- 🎨 **UI/UX**: Mejorar interfaz y experiencia de usuario

### Pull Request Process

1. **Actualiza el README.md** si cambias funcionalidad
2. **Actualiza la documentación** relevante
3. **Asegúrate de que los tests pasen**
4. **Describe tus cambios** claramente en el PR
5. **Espera revisión** de un mantenedor
6. **Responde a comentarios** y haz cambios si se requieren

#### Plantilla de Pull Request

```markdown
## Descripción
[Descripción de los cambios]

## Tipo de Cambio
- [ ] Bug fix
- [ ] Nueva característica
- [ ] Breaking change
- [ ] Documentación

## ¿Cómo se ha probado?
[Describe los tests realizados]

## Checklist
- [ ] Mi código sigue las guías de estilo
- [ ] He realizado self-review
- [ ] He comentado áreas complejas
- [ ] He actualizado la documentación
- [ ] Mis cambios no generan warnings
- [ ] He añadido tests
- [ ] Los tests nuevos y existentes pasan
```

### Tests

Ejemplo de test:
```python
import pytest
from src.core.command_processor import CommandProcessor

def test_process_punctuation():
    processor = CommandProcessor()
    result, is_action = processor.process_text("punto")
    assert result == "."
    assert is_action is False

def test_process_custom_command():
    processor = CommandProcessor()
    # Test implementation...
```

## Reconocimientos

Los contribuidores serán listados en el README.md y en el archivo CONTRIBUTORS.md.

## Preguntas

Si tienes preguntas, puedes:
- Abrir un issue con la etiqueta "question"
- Contactar a los mantenedores

¡Gracias por contribuir! 🎉
