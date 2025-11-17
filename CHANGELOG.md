# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-XX

### Añadido
- 🎤 Reconocimiento de voz continuo y por comando
- 🌍 Soporte multi-idioma (Español, Inglés, Francés, Alemán, Italiano, Portugués)
- ⌨️ Hotkeys globales configurables
- 🎯 Sistema de comandos personalizados
- 📝 Comandos de puntuación automática en español e inglés
- 🖥️ Interfaz gráfica PyQt5 con bandeja del sistema
- ⚙️ Diálogo de configuración completo
- 📋 Inserción automática de texto en aplicaciones activas
- 🔊 Retroalimentación de audio (beeps)
- 💾 Guardado automático de configuración
- 📄 Vista previa de texto reconocido
- 🚀 Inicio minimizado opcional
- 🔝 Opción de ventana siempre visible
- 📱 Notificaciones del sistema
- 🎨 Tema claro (preparado para tema oscuro)

### Características Técnicas
- Motor de reconocimiento de voz con Google Speech Recognition
- Soporte para Windows Speech Recognition (offline)
- Procesador de comandos extensible
- Gestor de atajos de teclado globales
- Sistema de configuración basado en JSON
- Arquitectura modular (GUI, Core, Utils)

### Comandos de Voz Incluidos

#### Puntuación (Español)
- "punto", "coma", "signo de interrogación", "signo de exclamación"
- "dos puntos", "punto y coma", "guión", "comillas"
- Símbolos especiales: "@", "#", "$", "%", etc.

#### Puntuación (Inglés)
- "period", "comma", "question mark", "exclamation mark"
- "colon", "semicolon", "dash", "quote"

#### Formato
- "nueva línea", "nuevo párrafo", "tabulación"
- "new line", "new paragraph", "tab"

#### Acciones
- "borrar última palabra", "borrar todo"
- "detener dictado", "pausar", "continuar"
- "delete last word", "delete all"

#### Comandos Personalizados (Ejemplos)
- Insertar fecha/hora actual
- Insertar texto predefinido (ej: email)
- Abrir URLs
- Simular pulsaciones de teclas

### Configuración

#### Parámetros de Reconocimiento
- Umbral de confianza ajustable (0.0 - 1.0)
- Umbral de energía de audio
- Ajuste dinámico de energía
- Umbral de pausa entre frases

#### Salida
- Inserción automática en app activa
- Opción de usar portapapeles
- Copia automática al portapapeles
- Retraso de pegado configurable

#### Avanzado
- Puntuación automática
- Capitalización automática
- Comandos personalizados habilitables
- Guardado de transcripciones

### Documentación
- README.md completo con ejemplos
- INSTALL.md con guía detallada de instalación
- CONTRIBUTING.md con guías de contribución
- Comentarios en código siguiendo estilo Google
- Configuración de ejemplo en JSON

### Requisitos del Sistema
- Windows 10/11
- Python 3.8+
- Micrófono funcional

### Dependencias Principales
- SpeechRecognition 3.10.1
- PyQt5 5.15.10
- keyboard 0.13.5
- pyperclip 1.8.2
- pyttsx3 2.90
- pywin32 306

## [Unreleased]

### Por Hacer
- [ ] Tema oscuro para la interfaz
- [ ] Soporte para más motores de reconocimiento (Whisper)
- [ ] Historial de transcripciones
- [ ] Editor de comandos personalizados en GUI
- [ ] Estadísticas de uso
- [ ] Exportar configuración
- [ ] Modo de entrenamiento de comandos
- [ ] Soporte para macros más complejas
- [ ] Integración con apps específicas (Word, Outlook, etc.)
- [ ] Corrección ortográfica integrada
- [ ] Sinónimos y sugerencias
- [ ] Modo dictado continuo mejorado
- [ ] Reconocimiento de voz offline con Whisper
- [ ] Perfiles de usuario múltiples
- [ ] Backup automático de configuración
- [ ] Actualizaciones automáticas
- [ ] Instalador Windows (.exe)
- [ ] Tests unitarios
- [ ] Tests de integración
- [ ] CI/CD con GitHub Actions

### Ideas Futuras
- 🤖 Integración con IA para corrección y sugerencias
- 🔌 Sistema de plugins
- ☁️ Sincronización en la nube
- 📱 Aplicación móvil complementaria
- 🎮 Modo gaming (comandos para juegos)
- 🎓 Modo académico (términos técnicos)
- 💼 Modo profesional (terminología empresarial)

---

## Tipos de Cambios

- **Añadido**: para nuevas características
- **Cambiado**: para cambios en funcionalidad existente
- **Obsoleto**: para características que serán removidas
- **Removido**: para características removidas
- **Corregido**: para corrección de bugs
- **Seguridad**: en caso de vulnerabilidades
