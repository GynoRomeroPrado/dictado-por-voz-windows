# 🎤 Dictado por Voz - Windows (Versión Simplificada)

**Dicta en CUALQUIER aplicación de Windows** - El texto se escribe directamente donde está el cursor.

## ✨ ¿Qué hace esta aplicación?

1. **Se ejecuta en segundo plano** (solo un icono en la bandeja del sistema)
2. **Presionas un hotkey** (por defecto: `Ctrl+Shift+Space`)
3. **Empiezas a hablar**
4. **El texto se escribe automáticamente** donde está el cursor del mouse
5. **Funciona en Word, Notepad, navegadores, emails, ¡CUALQUIER app!**

Es como tener **dictado universal** para Windows, similar a Voice In pero funcionando en **TODAS** las aplicaciones.

---

## 🚀 Instalación Rápida

### Opción 1: Con Poetry (Recomendado)

```bash
# Instalar dependencias
poetry install

# Ejecutar aplicación
poetry run python run_simple.py
```

### Opción 2: Con pip

```bash
# Instalar dependencias
pip install -r requirements-pyside6.txt

# Ejecutar aplicación
python run_simple.py
```

**IMPORTANTE**: En Windows, ejecuta como **Administrador** para que los hotkeys globales funcionen.

---

## 📖 Cómo Usar

### 1. Iniciar la Aplicación

```bash
python run_simple.py
```

Verás:
```
✓ Aplicación iniciada correctamente
✓ Presiona Ctrl+Shift+Space para iniciar dictado
```

### 2. Activar Dictado

1. **Abre cualquier aplicación** (Word, Notepad, Chrome, etc.)
2. **Coloca el cursor** donde quieras escribir
3. **Presiona `Ctrl+Shift+Space`**
4. **Habla claramente**
5. El texto se escribirá automáticamente

### 3. Detener Dictado

- Presiona `Ctrl+Shift+Space` nuevamente
- O haz clic derecho en el icono de la bandeja → "Detener"

---

## 🎯 Ejemplos de Uso

### Ejemplo 1: Escribir un Email en Gmail

1. Abre Gmail en tu navegador
2. Haz clic en "Redactar"
3. Coloca el cursor en el campo del mensaje
4. Presiona `Ctrl+Shift+Space`
5. Dicta: "Hola Juan coma nueva línea quería confirmar..."
6. El texto aparece automáticamente

### Ejemplo 2: Tomar Notas en Word

1. Abre Microsoft Word
2. Presiona `Ctrl+Shift+Space`
3. Dicta tus notas
4. Usa comandos de voz para puntuación:
   - "punto" → `.`
   - "coma" → `,`
   - "nueva línea" → ↵

### Ejemplo 3: Chatear en WhatsApp Web

1. Abre WhatsApp en el navegador
2. Selecciona un chat
3. Haz clic en el campo de texto
4. Presiona `Ctrl+Shift+Space`
5. Dicta tu mensaje
6. Presiona Enter para enviar

---

## 🎛️ Comandos de Voz

### Puntuación (Español)
- "punto" → `.`
- "coma" → `,`
- "signo de interrogación" → `?`
- "signo de exclamación" → `!`
- "dos puntos" → `:`
- "punto y coma" → `;`

### Puntuación (Inglés)
- "period" → `.`
- "comma" → `,`
- "question mark" → `?`
- "exclamation mark" → `!`

### Formato
- "nueva línea" / "new line" → ↵
- "nuevo párrafo" / "new paragraph" → ↵↵
- "tabulación" / "tab" → ⇥

### Acciones
- "borrar última palabra" → Elimina la última palabra
- "borrar todo" → Limpia el buffer
- "detener dictado" → Detiene el reconocimiento

---

## ⚙️ Configuración

### Cambiar el Hotkey

Edita `config/settings.json`:

```json
{
  "hotkeys": {
    "toggle_dictation": "ctrl+alt+d"
  }
}
```

Opciones de teclas:
- `ctrl+shift+space` (por defecto)
- `ctrl+alt+d`
- `alt+d`
- `win+d`
- etc.

### Cambiar el Idioma

```json
{
  "language": "en-US"
}
```

Idiomas soportados:
- `es-ES` (Español España)
- `es-MX` (Español México)
- `en-US` (English US)
- `en-GB` (English UK)
- `fr-FR` (Français)
- `de-DE` (Deutsch)
- Y más...

### Añadir Comandos Personalizados

Edita `config/commands.json`:

```json
{
  "custom_commands": [
    {
      "id": "mi_email",
      "enabled": true,
      "trigger": "mi correo",
      "action": "insert_text",
      "value": "tu@email.com"
    }
  ]
}
```

Ahora cuando digas "mi correo", escribirá `tu@email.com` automáticamente.

---

## 🔧 Solución de Problemas

### El hotkey no funciona

**Solución**: Ejecuta como Administrador

```powershell
# PowerShell (como Administrador)
python run_simple.py
```

### El micrófono no se detecta

1. Ve a Configuración de Windows → Privacidad → Micrófono
2. Asegúrate de que "Permitir que las aplicaciones accedan al micrófono" esté activado
3. Verifica que Python tenga permiso

### No reconoce mi voz

1. Habla más cerca del micrófono
2. Habla más despacio y claro
3. Reduce el ruido ambiental
4. Cambia el motor de reconocimiento en `config/settings.json`:

```json
{
  "recognition": {
    "engine": "google"
  }
}
```

### El texto no se escribe

1. Asegúrate de que el cursor esté en un campo de texto editable
2. Verifica que el módulo `keyboard` esté instalado
3. Ejecuta como Administrador

---

## 🆚 Comparación con Otras Soluciones

| Característica | Esta App | Voice In (Chrome) | Dragon |
|---------------|----------|-------------------|--------|
| **Funciona en todas las apps** | ✅ SÍ | ❌ Solo Chrome | ✅ SÍ |
| **Precio** | ✅ Gratis | $60/año | $300+ |
| **Hotkey global** | ✅ SÍ | ❌ NO | ✅ SÍ |
| **Open Source** | ✅ SÍ | ❌ NO | ❌ NO |
| **Ligero** | ✅ SÍ | ✅ SÍ | ❌ NO |
| **Offline** | ⚠️ Opcional | ❌ NO | ✅ SÍ |

---

## 💡 Tips y Trucos

### 1. Usar con Código
```
"función nueva línea
tabulación definir espacio hola
paréntesis izquierdo paréntesis derecho dos puntos
nueva línea tabulación return espacio verdadero"
```

### 2. Dictar Emails Rápidos
```
"Hola Juan coma nueva línea
te escribo para confirmar la reunión punto
nueva línea saludos coma
María"
```

### 3. Comandos Rápidos
Crea comandos personalizados para frases que uses mucho:
- "mi dirección" → Tu dirección completa
- "mi teléfono" → Tu número de teléfono
- "saludos cordiales" → Tu firma de email

---

## 📁 Estructura del Proyecto

```
dictado-por-voz-windows/
├── run_simple.py           ← EJECUTA ESTO
├── src/
│   ├── main_simple.py      ← Versión simplificada
│   ├── gui/
│   │   └── tray_icon.py    ← Solo icono de bandeja
│   └── core/
│       └── speech_recognizer.py
├── config/
│   ├── settings.json       ← Configuración
│   └── commands.json       ← Comandos personalizados
└── pyproject.toml         ← Configuración de Poetry
```

---

## 🤝 Contribuir

¿Encontraste un bug? ¿Tienes una sugerencia?

1. Abre un [Issue](https://github.com/GynoRomeroPrado/dictado-por-voz-windows/issues)
2. O envía un Pull Request

---

## 📝 Licencia

MIT License - Úsalo como quieras, es gratis y open source.

---

## 👤 Autor

**Gyno Romero Prado**

---

## 🙏 Agradecimientos

- Inspirado en [Voice In](https://dictanote.co/voicein/)
- Usa [SpeechRecognition](https://github.com/Uberi/speech_recognition)
- GUI con [PySide6](https://www.qt.io/qt-for-python)

---

## ❓ FAQ

### ¿Necesito internet?
Por defecto SÍ (usa Google Speech Recognition). Puedes cambiar a reconocimiento offline editando la configuración.

### ¿Funciona en Linux/Mac?
El código base sí, pero el módulo `keyboard` y los hotkeys globales están optimizados para Windows.

### ¿Puedo usarlo para programar?
Sí, pero es mejor desactivar auto-capitalización y crear comandos personalizados para símbolos comunes.

### ¿Es seguro?
Sí. Tu voz se procesa localmente o se envía a Google Speech (según configuración). Nada se guarda ni se comparte.

---

**¡Disfruta del dictado universal en Windows! 🎉**
