# 🎨 Interfaz Moderna - Dictado por Voz

Esta aplicación ahora cuenta con una interfaz completamente rediseñada con un diseño moderno, minimalista y no intrusivo.

## ✨ Características de la Nueva Interfaz

### 1. **Ventana Flotante de Grabación**

Cuando activas el dictado, aparece una pequeña ventana flotante que muestra el estado actual:

#### Modo Normal (`RecordingOverlay`)
- **Tamaño:** 220×70 px (muy pequeña y discreta)
- **Posición:** Esquina superior derecha (puede moverse arrastrándola)
- **Animación:** Punto rojo pulsante mientras graba
- **Estados:**
  - 🔴 **Escuchando...** - Grabando audio con pulso animado
  - ⚙️ **Procesando...** - Reconociendo y escribiendo texto
  - ❌ **Error** - Muestra mensajes de error temporalmente

#### Modo Minimalista (`MinimalRecordingIndicator`)
- **Tamaño:** 40×40 px (ultra compacto)
- **Diseño:** Solo un círculo rojo pulsante
- **Ideal para:** Usuarios que quieren la mínima distracción

**Cómo cambiar el modo:**
Edita `config/config.ini`:
```ini
[ui]
minimal_indicator = false  # false = modo normal, true = modo minimalista
```

### 2. **Diálogo de Configuración Rápida Rediseñado**

Interfaz moderna con diseño limpio y organizado:

**Características:**
- ✨ Sin marco de ventana tradicional (frameless)
- 🎨 Diseño oscuro moderno (dark theme)
- 📱 Layout limpio con secciones bien definidas
- 🖱️ Se puede mover arrastrando desde cualquier parte
- 💾 Guarda automáticamente los cambios

**Secciones:**
1. **🌍 Idioma** - Selector de idioma con 8 idiomas disponibles
2. **⌨️ Atajos** - Configura la combinación de teclas
3. **🚀 Auto-inicio** - Checkbox para iniciar con Windows
4. **🔔 Notificaciones** - Control de notificaciones y sonidos

**Acceso:**
- Click derecho en icono de bandeja → "⚙ Configuración Rápida"
- Atajo: Ctrl+Alt+S (configurable)

### 3. **Sistema de Estilos Modernos**

**Paleta de colores:**
- **Dark Theme** (tema oscuro por defecto)
  - Primary: #6366F1 (Indigo vibrante)
  - Background: #0F172A (Slate 900)
  - Text: #F1F5F9 (Slate claro)

- **Light Theme** (tema claro disponible)
  - Primary: #6366F1
  - Background: #FFFFFF
  - Text: #0F172A

**Elementos de diseño:**
- ✅ Esquinas redondeadas (8-16px radius)
- ✅ Sombras sutiles para profundidad
- ✅ Transiciones suaves
- ✅ Tipografía moderna (Inter, Segoe UI, SF Pro)
- ✅ Botones con estados hover/pressed
- ✅ Inputs con focus states
- ✅ Checkboxes y controles personalizados

## 🎯 Flujo de Uso

### Grabación Visual

```
1. Usuario presiona Ctrl+Shift+Space
   ↓
2. Aparece ventana flotante "Escuchando..."
   - Punto rojo pulsando
   - Texto: "Presiona Ctrl+Shift+Space para detener"
   ↓
3. Usuario habla
   ↓
4. Ventana cambia a "Procesando..."
   - Se detiene el pulso
   - Texto: "Escribiendo texto..."
   ↓
5. Texto se escribe donde está el cursor
   ↓
6. Ventana se oculta automáticamente (2 segundos)
   O usuario presiona el atajo de nuevo
```

### Configuración

```
1. Click derecho en icono de bandeja
   ↓
2. Seleccionar "⚙ Configuración Rápida"
   ↓
3. Aparece diálogo moderno
   - Sin marco tradicional
   - Diseño oscuro
   - Botón X para cerrar
   ↓
4. Cambiar configuración
   - Los cambios se guardan automáticamente
   ↓
5. Click en "Guardar cambios" o presionar X
```

## 🎨 Comparación: Antes vs Ahora

### Antes ❌
- Ventana grande con preview de texto
- Interfaz con marcos tradicionales
- Colores básicos
- Sin animaciones
- Interfaz intrusiva

### Ahora ✅
- Ventana flotante pequeña (220×70 o 40×40)
- Sin marcos (frameless)
- Paleta de colores moderna
- Animaciones suaves (pulso, transiciones)
- Minimalista y discreta

## 🛠️ Personalización

### Cambiar Tema

Edita `src/main_simple.py`:
```python
# Línea 71 - Cambiar tema del overlay
self.recording_overlay = RecordingOverlay(theme='dark')  # o 'light'

# Línea 171 - Cambiar tema de configuración rápida
self.quick_settings_dialog = QuickSettingsDialog(theme='dark')  # o 'light'
```

### Cambiar Posición de la Ventana Flotante

Edita `src/gui/recording_overlay.py`, método `position_window()`:
```python
def position_window(self):
    """Posiciona la ventana"""
    from PySide6.QtGui import QGuiApplication
    screen = QGuiApplication.primaryScreen().geometry()

    # Esquina superior derecha (por defecto)
    x = screen.width() - self.width() - 20
    y = 20

    # Otras opciones:
    # Esquina superior izquierda
    # x = 20
    # y = 20

    # Centro superior
    # x = (screen.width() - self.width()) // 2
    # y = 20

    # Esquina inferior derecha
    # x = screen.width() - self.width() - 20
    # y = screen.height() - self.height() - 60

    self.move(x, y)
```

### Personalizar Colores

Edita `src/gui/modern_styles.py`, diccionario `COLORS`:
```python
COLORS = {
    'dark': {
        'primary': '#6366F1',      # Tu color primario
        'bg_primary': '#0F172A',   # Color de fondo
        'text_primary': '#F1F5F9', # Color de texto
        # ... más colores
    }
}
```

### Cambiar Tamaño de Ventana Flotante

Edita `src/gui/recording_overlay.py`, método `__init__()`:
```python
# Línea 45 - Cambiar tamaño
self.setFixedSize(220, 70)  # Ancho, Alto en píxeles

# Para hacerla más grande:
self.setFixedSize(300, 100)

# Para hacerla más pequeña:
self.setFixedSize(180, 60)
```

## 📱 Modos de Visualización

### Modo 1: Overlay Completo (Por defecto)
```ini
[ui]
minimal_indicator = false
```
- Muestra texto de estado
- Animación de pulso
- Instrucciones de atajo
- Mensajes de error

### Modo 2: Indicador Minimalista
```ini
[ui]
minimal_indicator = true
```
- Solo círculo rojo
- Pulsa mientras graba
- Sin texto
- Ultra discreto

### Modo 3: Sin Indicador Visual (Futuro)
Para usuarios que solo quieren el beep de audio:
```ini
[ui]
show_recording_indicator = false
```

## 🎨 Guía de Colores

### Colores de Estado

| Estado | Color | Uso |
|--------|-------|-----|
| Primary | #6366F1 Indigo | Botones principales, acciones |
| Success | #10B981 Green | Operaciones exitosas |
| Danger | #EF4444 Red | Errores, detener grabación |
| Warning | #F59E0B Amber | Advertencias |
| Secondary | #8B5CF6 Purple | Acciones secundarias |

### Colores de Fondo (Dark)

| Elemento | Color | Hex |
|----------|-------|-----|
| Primario | Slate 900 | #0F172A |
| Secundario | Slate 800 | #1E293B |
| Terciario | Slate 700 | #334155 |

### Colores de Texto (Dark)

| Elemento | Color | Hex |
|----------|-------|-----|
| Principal | Slate 100 | #F1F5F9 |
| Secundario | Slate 400 | #94A3B8 |

## 🚀 Rendimiento

### Optimizaciones

1. **Ventana Flotante**
   - Solo se crea una vez al iniciar
   - Se oculta/muestra en lugar de crear/destruir
   - Animaciones con QPropertyAnimation (aceleradas por GPU)

2. **Estilos**
   - Stylesheet cargado una sola vez
   - Reutilizado en todos los componentes
   - Sin recálculo dinámico

3. **Memoria**
   - Overlay: ~2-3 MB
   - Configuración: ~1-2 MB
   - Total adicional: ~5 MB

## 📝 Notas Técnicas

### Tecnologías Usadas

- **PySide6** - Framework Qt para Python
- **QPropertyAnimation** - Animaciones suaves
- **QSS** (Qt Style Sheets) - Estilos CSS-like
- **Frameless Windows** - Ventanas sin marco

### Compatibilidad

- ✅ Windows 10+
- ✅ Soporte para múltiples monitores
- ✅ Escalado DPI automático
- ✅ Temas oscuro y claro

### Archivos de Interfaz

```
src/gui/
├── modern_styles.py        # Sistema de estilos modernos
├── recording_overlay.py    # Ventana flotante de grabación
├── quick_settings.py       # Configuración rápida (rediseñado)
├── tray_icon.py           # Icono de bandeja
├── main_window.py         # Ventana antigua (deprecado)
└── settings_dialog.py     # Configuración completa (deprecado)
```

## 🎯 Próximas Mejoras

- [ ] Selector de tema (oscuro/claro) en configuración
- [ ] Más posiciones predefinidas para overlay
- [ ] Personalización de colores desde UI
- [ ] Animaciones adicionales
- [ ] Soporte para iconos personalizados
- [ ] Temas predefinidos (Discord-like, VS Code-like, etc.)

---

**¿Preguntas o sugerencias?**
Esta es la nueva interfaz moderna y minimalista. Todo está diseñado para ser discreto pero funcional.
