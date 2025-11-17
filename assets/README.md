# Assets Directory

Esta carpeta contiene recursos gráficos para la aplicación.

## Icono de la Aplicación

Para agregar un icono personalizado:

1. **Crear o descargar un icono en formato .ico**
   - El icono debe ser de al menos 256x256 píxeles
   - Formato recomendado: .ico (Windows Icon)
   - Debe contener múltiples tamaños: 16x16, 32x32, 48x48, 256x256

2. **Guardar el icono**
   - Nombre del archivo: `icon.ico`
   - Ubicación: Coloca el archivo en esta carpeta (`assets/icon.ico`)

3. **Actualizar las referencias**
   - El archivo `build.spec` ya está configurado para usar `assets/icon.ico`
   - El archivo `installer.iss` ya está configurado para usar `assets/icon.ico`

4. **Volver a compilar**
   - Ejecuta `python build.py` para generar el .exe con el nuevo icono
   - Ejecuta `iscc installer.iss` para generar el instalador con el nuevo icono

## Herramientas para Crear Iconos

### Online
- [favicon.io](https://favicon.io/) - Genera iconos desde imágenes, texto o emojis
- [icoconvert.com](https://icoconvert.com/) - Convierte imágenes a formato .ico

### Software
- **GIMP** (Gratis) - Con plugin ICO
- **IrfanView** (Gratis) - Puede guardar en formato .ico
- **Adobe Photoshop** - Con plugin ICO

## Diseño Sugerido

Para un icono de dictado por voz, considera:
- 🎤 Un micrófono
- 💬 Un bocadillo de diálogo
- 🔊 Ondas de sonido
- 🗣️ Una boca hablando
- Colores: Azul, verde o rojo para indicar estado activo

## Sin Icono Personalizado

Si no agregas un icono personalizado:
- **Durante desarrollo**: La aplicación usará el icono predeterminado de Python/Windows
- **Build sin icono**: El .exe funcionará perfectamente, solo usará el icono genérico
- **Para build temporales**: Puedes comentar la línea `icon=` en `build.spec` e `installer.iss`

## Ejemplo de Icono Simple

Si quieres un icono rápido para pruebas, puedes:
1. Buscar "microphone icon free" en Google Images
2. Usar un emoji convertido a imagen (🎤)
3. Usar herramientas online para generar desde texto o emoji
