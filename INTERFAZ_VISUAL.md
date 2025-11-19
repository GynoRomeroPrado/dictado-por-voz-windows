# 🎨 Vista Previa de la Nueva Interfaz Moderna

## 📱 Ventana Flotante de Grabación

### Modo Normal (220×70 px)

```
╔══════════════════════════════════════════╗
║  🔴 Escuchando...                        ║
║  Presiona Ctrl+Shift+Space para detener  ║
╚══════════════════════════════════════════╝
```

**Características:**
- **Posición:** Esquina superior derecha (movible)
- **Color de fondo:** Slate oscuro (#1E293B)
- **Borde:** Indigo brillante (#6366F1)
- **Animación:** El punto rojo 🔴 pulsa suavemente (1s fade in/out)
- **Esquinas:** Redondeadas (16px)
- **Transparencia:** Semi-transparente con sombra

**Estados:**

1. **Escuchando**
```
╔══════════════════════════════════════════╗
║  🔴 Escuchando...                        ║
║  Presiona Ctrl+Shift+Space para detener  ║
╚══════════════════════════════════════════╝
```

2. **Procesando**
```
╔══════════════════════════════════════════╗
║  🔴 Procesando...                        ║
║  Escribiendo texto...                    ║
╚══════════════════════════════════════════╝
```

3. **Error**
```
╔══════════════════════════════════════════╗
║  🔴 Error al reconocer                   ║
║  Intenta de nuevo                        ║
╚══════════════════════════════════════════╝
```

### Modo Minimalista (40×40 px)

```
   ╔════╗
   ║ 🔴 ║
   ╚════╝
```

**Características:**
- **Solo un círculo rojo pulsante**
- **Ultra compacto**
- **Sin texto**
- **Perfecto para no distraer**

---

## ⚙ Diálogo de Configuración Rápida

### Vista Completa (480 px ancho)

```
╔════════════════════════════════════════════════════════════╗
║  ⚙ Configuración                                      [✕] ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  🌍 Idioma de reconocimiento                              ║
║  Selecciona el idioma para el reconocimiento de voz       ║
║  ┌──────────────────────────────────────────────────┐    ║
║  │ Español (España)                            ▼    │    ║
║  └──────────────────────────────────────────────────┘    ║
║                                                            ║
║  ⌨️ Atajo de teclado                                      ║
║  Presiona esta combinación para iniciar/detener el dictado║
║  ┌──────────────────────────────────────────────────┐    ║
║  │ ctrl+shift+space                                 │    ║
║  └──────────────────────────────────────────────────┘    ║
║  💡 Ejemplos: ctrl+shift+space, alt+d, ctrl+alt+v        ║
║                                                            ║
║  🚀 Inicio automático                                     ║
║  ☑ Iniciar automáticamente con Windows                   ║
║                                                            ║
║  🔔 Notificaciones                                        ║
║  ☑ Mostrar notificaciones                                ║
║  ☑ Reproducir sonidos                                    ║
║                                                            ║
╠════════════════════════════════════════════════════════════╣
║  [Restaurar valores predeterminados]  [Guardar cambios]  ║
╚════════════════════════════════════════════════════════════╝
```

**Características:**
- **Sin marco tradicional:** Diseño frameless moderno
- **Header:** Título grande con botón X elegante
- **Secciones:** Bien separadas con títulos en negrita
- **Colores:**
  - Fondo: Slate oscuro (#0F172A, #1E293B)
  - Texto: Blanco suave (#F1F5F9)
  - Inputs: Slate más claro con borde
  - Primario: Indigo (#6366F1)
- **Tipografía:** Inter, Segoe UI, moderna y limpia
- **Controles:** Personalizados con animaciones hover

---

## 🎨 Paleta de Colores Visual

### Colores Principales

```
┌─────────────────────┐
│ Primary (Indigo)    │  ████  #6366F1
│ Hover               │  ████  #818CF8
│ Pressed             │  ████  #4F46E5
└─────────────────────┘

┌─────────────────────┐
│ Success (Green)     │  ████  #10B981
│ Danger (Red)        │  ████  #EF4444
│ Warning (Amber)     │  ████  #F59E0B
└─────────────────────┘
```

### Fondos (Dark Theme)

```
┌─────────────────────┐
│ Background Primary  │  ████  #0F172A  (Slate 900)
│ Background Secondary│  ████  #1E293B  (Slate 800)
│ Background Tertiary │  ████  #334155  (Slate 700)
└─────────────────────┘
```

### Textos (Dark Theme)

```
┌─────────────────────┐
│ Text Primary        │  ████  #F1F5F9  (Casi blanco)
│ Text Secondary      │  ████  #94A3B8  (Gris claro)
└─────────────────────┘
```

---

## 🖱️ Interacciones

### Botones

**Estado Normal:**
```
┌─────────────────────┐
│   Guardar cambios   │  [Indigo sólido]
└─────────────────────┘
```

**Estado Hover:**
```
┌─────────────────────┐
│   Guardar cambios   │  [Indigo más claro, cursor pointer]
└─────────────────────┘
```

**Estado Pressed:**
```
┌─────────────────────┐
│   Guardar cambios   │  [Indigo más oscuro]
└─────────────────────┘
```

### Inputs

**Estado Normal:**
```
┌──────────────────────────────────────┐
│ ctrl+shift+space                     │  [Fondo Slate, borde gris]
└──────────────────────────────────────┘
```

**Estado Focus:**
```
┌══════════════════════════════════════┐
│ ctrl+shift+space█                    │  [Borde Indigo brillante]
└══════════════════════════════════════┘
```

### Checkboxes

**No marcado:**
```
☐ Iniciar con Windows
```

**Marcado:**
```
☑ Iniciar con Windows  [Checkbox Indigo con check blanco]
```

**Hover:**
```
☐ Iniciar con Windows  [Borde Indigo]
```

---

## 💫 Animaciones

### 1. Pulso del Punto Rojo

```
Tiempo:  0s    0.5s    1s
         ●  →  ◐  →   ○  →  ◐  →  ●
Opacidad: 100%  65%   30%   65%  100%
```

**Duración:** 1 segundo
**Loop:** Infinito
**Easing:** InOutSine (suave)

### 2. Transición de Botones

```
Normal → Hover
├─ Duración: 200ms
├─ Propiedad: background-color
└─ Easing: ease-in-out
```

### 3. Aparición de Ventana Flotante

```
Oculta → Visible
├─ Duración: 300ms
├─ Propiedades: opacity, scale
└─ Efecto: Fade in + scale up
```

---

## 📐 Dimensiones y Espaciado

### Ventana Flotante (Modo Normal)

```
┌────────────────────────────┐
│                            │
│  ← 220 px →                │
│  ↑                         │
│  70px                      │
│  ↓                         │
│                            │
└────────────────────────────┘

Padding: 16px (horizontal), 12px (vertical)
Border: 2px solid Indigo
Border-radius: 16px
```

### Ventana Flotante (Modo Minimalista)

```
┌─────┐
│     │  ← 40 px →
│  ●  │
│     │
└─────┘
   ↑
  40px
   ↓

Border-radius: 20px (círculo)
```

### Diálogo de Configuración

```
┌──────────────────────────────────────────┐
│  ← 480 px (fijo) →                       │
│  ↑                                       │
│  Auto (según contenido)                  │
│  ↓                                       │
└──────────────────────────────────────────┘

Header height: 60px
Content padding: 24px
Section spacing: 20px
Footer height: 56px
```

---

## 🎯 Flujo Visual

### Usuario Inicia Dictado

```
1. Usuario presiona Ctrl+Shift+Space
          ↓
2. [Aparece overlay con fade-in]
          ↓
   ╔══════════════════════════════╗
   ║  🔴 Escuchando...            ║
   ║  Presiona... para detener    ║
   ╚══════════════════════════════╝
          ↓
3. [Punto rojo pulsa 1s loop]
   ● → ◐ → ○ → ◐ → ● → ...
          ↓
4. Usuario habla: "Hola mundo"
          ↓
5. [Overlay cambia estado]
          ↓
   ╔══════════════════════════════╗
   ║  🔴 Procesando...            ║
   ║  Escribiendo texto...        ║
   ╚══════════════════════════════╝
          ↓
6. Texto se escribe: "Hola mundo"
          ↓
7. [Overlay desaparece con fade-out después de 2s]
```

### Usuario Abre Configuración

```
1. Click derecho en icono de bandeja
          ↓
2. Menu aparece:
   ┌────────────────────────┐
   │ ▶ Iniciar Dictado      │
   │ ⚙ Configuración Rápida │  ← Click aquí
   │ ...                    │
   └────────────────────────┘
          ↓
3. [Diálogo aparece centrado]
          ↓
   ╔═══════════════════════════╗
   ║  ⚙ Configuración     [✕] ║
   ║  ...                      ║
   ╚═══════════════════════════╝
          ↓
4. Usuario hace cambios
          ↓
5. Click en "Guardar cambios"
          ↓
6. [Diálogo desaparece con fade-out]
```

---

## 🆚 Comparación Visual

### Antes (Interfaz Antigua)

```
╔═══════════════════════════════════════════╗
║  Dictado por Voz - Windows            [_][[]]║
╠═══════════════════════════════════════════╣
║  [Iniciar]  [Detener]  [Configurar]      ║
╠═══════════════════════════════════════════╣
║  ┌─────────────────────────────────────┐ ║
║  │                                     │ ║
║  │  [Vista previa de texto aquí]      │ ║
║  │                                     │ ║
║  │                                     │ ║
║  └─────────────────────────────────────┘ ║
║                                           ║
║  Estado: Detenido                         ║
║  Idioma: [Español ▼]                      ║
╚═══════════════════════════════════════════╝
```

**Problemas:**
- ❌ Grande y ocupa espacio
- ❌ Marcos tradicionales
- ❌ Colores básicos
- ❌ Sin animaciones
- ❌ Intrusiva

### Ahora (Interfaz Moderna)

```
Solo visible mientras graba:

╔══════════════════════════════════════════╗
║  🔴 Escuchando...                        ║
║  Presiona Ctrl+Shift+Space para detener  ║
╚══════════════════════════════════════════╝
```

**Ventajas:**
- ✅ Pequeña (220×70 px)
- ✅ Sin marcos (frameless)
- ✅ Colores modernos
- ✅ Animación suave
- ✅ No intrusiva
- ✅ Solo aparece cuando es necesario

---

## 🎨 Tipografía

### Fuentes Usadas

```
Prioridad de fuentes:
1. Inter (moderna, geométrica)
2. Segoe UI (Windows nativa)
3. SF Pro (Apple-like)
4. Roboto (Android-like)
5. Sans-serif (fallback)
```

### Tamaños de Texto

```
Título (Header):           18px  (Bold)
Título de Sección:         12px  (Bold)
Texto Normal:              13px  (Regular)
Texto Secundario:          12px  (Regular)
Hint/Descripción:          11px  (Regular)
```

---

## 🌟 Detalles de Diseño

### Esquinas Redondeadas

```
Ventana flotante:    16px  (muy redondeadas)
Diálogo:            12px  (redondeadas)
Botones:             8px  (suavemente redondeadas)
Inputs:              6px  (ligeramente redondeadas)
Checkboxes:          4px  (sutilmente redondeadas)
```

### Sombras

```
Ventana flotante:    0 4px 12px rgba(0,0,0,0.3)
Diálogo:            0 8px 24px rgba(0,0,0,0.2)
Botones (hover):    0 2px 8px rgba(99,102,241,0.3)
```

### Bordes

```
Ventana flotante:    2px solid Indigo
Inputs (focus):     2px solid Indigo
Inputs (normal):    1px solid Slate
Separadores:        1px solid Slate
```

---

**Esta es la nueva interfaz moderna!** 🎨✨

Diseño inspirado en aplicaciones modernas como Discord, Notion, y VS Code,
con un toque minimalista y profesional.
