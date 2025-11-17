# Dictado por Voz - Windows Desktop App

Una aplicación de escritorio para Windows que permite dictar texto usando reconocimiento de voz en cualquier aplicación, inspirada en la extensión Voice In de Chrome.

## Características Principales

- **Reconocimiento de Voz Universal**: Dicta en cualquier aplicación de Windows
- **Procesamiento Local**: Todo el audio se procesa en tu computadora (privacidad total)
- **Multi-idioma**: Soporte para español, inglés y más de 20 idiomas
- **Comandos Personalizados**: Crea atajos de voz para texto y acciones
- **Hotkeys Globales**: Activa el dictado con atajos de teclado desde cualquier aplicación
- **Puntuación Automática**: Comandos de voz para puntuación y formato
- **Interfaz Simple**: GUI minimalista y fácil de usar
- **Bandeja del Sistema**: Se ejecuta en segundo plano

## Requisitos

- Windows 10/11
- Python 3.8 o superior
- Micrófono funcional

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/GynoRomeroPrado/dictado-por-voz-windows.git
cd dictado-por-voz-windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python src/main.py
```

## Uso Rápido

1. **Iniciar la aplicación**: Ejecuta `python src/main.py`
2. **Activar dictado**: Presiona `Ctrl+Shift+Space` (configurable)
3. **Hablar**: Di tu texto claramente
4. **Detener**: Presiona nuevamente `Ctrl+Shift+Space` o di "detener dictado"

## Comandos de Voz Predefinidos

### Puntuación
- "punto" → `.`
- "coma" → `,`
- "signo de interrogación" → `?`
- "signo de exclamación" → `!`
- "dos puntos" → `:`
- "punto y coma" → `;`
- "nueva línea" → Salto de línea
- "nuevo párrafo" → Doble salto de línea

### Acciones
- "borrar última palabra" → Elimina la última palabra
- "borrar todo" → Limpia el buffer actual
- "detener dictado" → Detiene el reconocimiento

## Comandos Personalizados

Puedes crear tus propios comandos editando `config/commands.json`:

```json
{
  "custom_commands": [
    {
      "trigger": "mi correo",
      "action": "insert_text",
      "value": "micorreo@ejemplo.com"
    },
    {
      "trigger": "abrir navegador",
      "action": "open_url",
      "value": "https://www.google.com"
    },
    {
      "trigger": "fecha actual",
      "action": "insert_date",
      "format": "%d/%m/%Y"
    }
  ]
}
```

## Configuración

Edita `config/settings.json` para personalizar:

- **Idioma de reconocimiento**: `es-ES`, `en-US`, etc.
- **Hotkey global**: Combinación de teclas para activar
- **Confianza mínima**: Umbral de precisión (0.0 - 1.0)
- **Inserción automática**: Insertar en app activa o copiar al portapapeles

## Arquitectura del Proyecto

```
dictado-por-voz-windows/
├── src/
│   ├── main.py                    # Punto de entrada
│   ├── gui/                       # Interfaz gráfica
│   │   ├── main_window.py         # Ventana principal
│   │   └── settings_dialog.py     # Diálogo de configuración
│   ├── core/                      # Lógica principal
│   │   ├── speech_recognizer.py   # Motor de reconocimiento
│   │   ├── command_processor.py   # Procesador de comandos
│   │   └── hotkey_manager.py      # Gestor de hotkeys
│   └── utils/                     # Utilidades
│       ├── config.py              # Gestor de configuración
│       └── clipboard.py           # Utilidades de portapapeles
├── config/
│   ├── settings.json              # Configuración de usuario
│   └── commands.json              # Comandos personalizados
├── requirements.txt
└── README.md
```

## Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal
- **SpeechRecognition**: Reconocimiento de voz (Windows Speech API)
- **PyQt5**: Interfaz gráfica moderna
- **keyboard**: Hotkeys globales
- **pyttsx3**: Síntesis de voz (feedback)
- **pyperclip**: Manejo de portapapeles

## Comparación con Voice In

| Característica | Voice In (Chrome) | Esta App (Windows) |
|---------------|-------------------|-------------------|
| Plataforma | Solo Chrome | Todas las apps de Windows |
| Procesamiento | Local en navegador | Local en Windows |
| Precio | Gratis/$60/año | Gratis y Open Source |
| Comandos personalizados | ✓ Plus | ✓ Gratis |
| Hotkeys globales | ✗ | ✓ |
| Bandeja del sistema | ✗ | ✓ |

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

MIT License - ve el archivo [LICENSE](LICENSE) para más detalles.

## Autor

**Gyno Romero Prado**

## Agradecimientos

- Inspirado en la extensión [Voice In](https://dictanote.co/voicein/) para Chrome
- Windows Speech Recognition API
- Comunidad Open Source de Python
