# Inicio Rápido - Dictado por Voz Windows

¿Quieres empezar a usar la aplicación en 5 minutos? Sigue esta guía.

## 🚀 Instalación Express (5 minutos)

```bash
# 1. Clonar repositorio
git clone https://github.com/GynoRomeroPrado/dictado-por-voz-windows.git
cd dictado-por-voz-windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar aplicación
python run.py
```

## 🎤 Primer Uso

### 1. Configurar Micrófono
- Asegúrate de que tu micrófono esté conectado
- Windows te pedirá permiso la primera vez
- La app ajustará automáticamente el ruido ambiente

### 2. Seleccionar Idioma
- En la ventana principal, selecciona tu idioma preferido
- Opciones: Español (España), Español (México), English, etc.

### 3. Iniciar Dictado
Hay dos formas:
- **Método 1**: Haz clic en el botón "▶ Iniciar Dictado"
- **Método 2**: Presiona `Ctrl+Shift+Space` desde cualquier aplicación

### 4. Dictar
- Habla claramente en tu micrófono
- El texto aparecerá automáticamente en la aplicación activa
- También verás una vista previa en la ventana de la app

### 5. Detener
- Haz clic en "⏹ Detener"
- O presiona `Ctrl+Shift+Space` nuevamente

## 📝 Ejemplos de Uso

### Ejemplo 1: Escribir un Email

```
[Activa dictado en tu cliente de correo]

"Hola Juan coma nueva línea nueva línea
Te escribo para confirmar la reunión de mañana a las diez punto
¿Podrías traer los documentos que discutimos? exclamación
nueva línea nueva línea
Saludos coma nueva línea
María"
```

**Resultado:**
```
Hola Juan,

Te escribo para confirmar la reunión de mañana a las diez.
¿Podrías traer los documentos que discutimos?

Saludos,
María
```

### Ejemplo 2: Tomar Notas Rápidas

```
"Reunión del proyecto guión fecha actual
nueva línea nueva línea
Participantes dos puntos Juan coma María coma Pedro
nueva línea nueva línea
Temas a tratar dos puntos
nueva línea guión Presupuesto
nueva línea guión Timeline
nueva línea guión Recursos"
```

### Ejemplo 3: Programar (con comandos personalizados)

Primero configura comandos en `config/commands.json`:
```json
{
  "trigger": "función",
  "action": "insert_text",
  "value": "def function_name():\n    pass"
}
```

Luego dicta:
```
"función nueva línea tabulación return True"
```

## 🎯 Comandos Más Usados

### Puntuación
| Comando | Resultado |
|---------|-----------|
| "punto" | `.` |
| "coma" | `,` |
| "signo de interrogación" | `?` |
| "signo de exclamación" | `!` |
| "nueva línea" | ↵ |
| "nuevo párrafo" | ↵↵ |

### Acciones
| Comando | Acción |
|---------|--------|
| "borrar última palabra" | Elimina la última palabra |
| "borrar todo" | Limpia el buffer |
| "pausar" | Pausa el dictado |
| "continuar" | Reanuda el dictado |

## ⚙️ Configuración Rápida

### Cambiar Hotkey
1. Haz clic en "⚙ Configuración"
2. Ve a la pestaña "Atajos de Teclado"
3. Cambia la combinación (ej: `alt+d`)
4. Haz clic en "Guardar"

### Ajustar Precisión
Si el reconocimiento no es preciso:
1. Ve a Configuración → Reconocimiento
2. Ajusta "Umbral de energía":
   - Aumenta si capta mucho ruido de fondo
   - Disminuye si no capta tu voz
3. Ajusta "Confianza mínima":
   - Aumenta para mayor precisión (pero menos palabras)
   - Disminuye para captar más (pero puede haber errores)

### Modo Clipboard (si la inserción automática no funciona)
1. Ve a Configuración → Salida
2. Marca "Usar portapapeles para insertar"
3. El texto se copiará al portapapeles y se pegará automáticamente

## 🔧 Solución Rápida de Problemas

### "No reconoce mi voz"
- Habla más cerca del micrófono
- Reduce el ruido ambiental
- Aumenta el volumen del micrófono en Windows
- Cambia el motor de reconocimiento a "Google"

### "El texto no se inserta"
- Asegúrate de que hay una aplicación activa con un campo de texto
- Prueba el modo portapapeles (ver arriba)
- Verifica que no haya otra app bloqueando la entrada

### "Error al iniciar"
- Verifica que PyQt5 esté instalado: `pip install PyQt5`
- Verifica permisos del micrófono en Windows
- Ejecuta como administrador si hay problemas con hotkeys

## 💡 Tips y Trucos

### 1. Bandeja del Sistema
- La app se minimiza a la bandeja del sistema
- Haz doble clic en el icono para mostrar/ocultar
- Clic derecho para menú rápido

### 2. Comandos Personalizados
Crea atajos para texto que usas frecuentemente:
- Tu email
- Tu dirección
- Frases comunes
- Firmas

Edita `config/commands.json`:
```json
{
  "trigger": "mi email",
  "action": "insert_text",
  "value": "tu@email.com"
}
```

### 3. Múltiples Idiomas
Puedes cambiar el idioma sobre la marcha:
- Selecciona el idioma en el dropdown
- O crea un comando personalizado: "cambiar a inglés"

### 4. Trabajar con Código
Para programar, es útil:
- Desactivar capitalización automática
- Crear comandos para snippets comunes
- Usar modo portapapeles

## 📱 Casos de Uso

### Para Escritores
- Dictar borradores rápidamente
- Comandos para formato (negrita, cursiva)
- Insertar fechas y timestamps

### Para Estudiantes
- Tomar notas de clase
- Transcribir lecturas
- Crear resúmenes rápidos

### Para Profesionales
- Dictar emails
- Llenar formularios
- Documentar reuniones

### Para Personas con Discapacidad
- Navegación manos libres
- Dictado accesible
- Comandos personalizados para necesidades específicas

## 🎓 Siguiente Paso

- Lee el [README.md](README.md) completo para características avanzadas
- Revisa [INSTALL.md](INSTALL.md) para configuración detallada
- Personaliza tus comandos en `config/commands.json`
- Explora la configuración en `config/settings.json`

## 🆘 Necesitas Ayuda?

- 📖 Lee la documentación completa
- 🐛 Reporta bugs en [GitHub Issues](https://github.com/GynoRomeroPrado/dictado-por-voz-windows/issues)
- 💬 Pregunta en las Discussions

---

¡Listo! Ya estás dictando por voz en Windows 🎉
