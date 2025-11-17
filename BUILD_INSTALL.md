# 🔨 Guía de Build e Instalación - Dictado por Voz

Esta guía explica cómo compilar el ejecutable (.exe) y crear el instalador para Windows.

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Instalación de Dependencias](#instalación-de-dependencias)
3. [Compilar el Ejecutable](#compilar-el-ejecutable)
4. [Crear el Instalador](#crear-el-instalador)
5. [Distribución](#distribución)
6. [Solución de Problemas](#solución-de-problemas)

---

## 🔧 Requisitos Previos

### Software Necesario

1. **Python 3.10 o superior**
   - Descarga: https://www.python.org/downloads/
   - ✅ Marca "Add Python to PATH" durante la instalación

2. **PyInstaller** (para crear el .exe)
   ```bash
   pip install pyinstaller
   ```

3. **Inno Setup** (para crear el instalador) - OPCIONAL
   - Descarga: https://jrsoftware.org/isdl.php
   - Versión recomendada: 6.2.2 o superior
   - Solo necesario si quieres crear un instalador profesional

### Verificar Instalación

```bash
# Verificar Python
python --version
# Debe mostrar: Python 3.10.x o superior

# Verificar pip
pip --version

# Verificar PyInstaller
pyinstaller --version
# Debe mostrar: 5.x o superior
```

---

## 📦 Instalación de Dependencias

### Opción 1: Usando Poetry (Recomendado)

```bash
# Instalar Poetry si no lo tienes
pip install poetry

# Instalar dependencias del proyecto
poetry install
```

### Opción 2: Usando pip

```bash
# Instalar dependencias desde requirements
pip install -r requirements-pyside6.txt

# Instalar PyInstaller
pip install pyinstaller
```

### Verificar Dependencias

```bash
python -c "import PySide6; import speech_recognition; import keyboard; print('✓ Todo OK')"
```

---

## 🏗️ Compilar el Ejecutable

### Método Automático (Recomendado)

Usa el script de build incluido:

```bash
# Build completo (limpia + compila)
python build.py

# Build con limpieza explícita
python build.py --clean
```

El script hará:
1. ✅ Verificar dependencias
2. ✅ Limpiar builds anteriores
3. ✅ Compilar con PyInstaller
4. ✅ Crear carpeta de distribución
5. ✅ Copiar archivos necesarios

**Resultado:** El ejecutable estará en `dist/DictadoPorVoz.exe`

### Método Manual

Si prefieres controlar el proceso manualmente:

```bash
# 1. Limpiar builds anteriores
rmdir /s /q build dist

# 2. Compilar con PyInstaller usando el spec file
pyinstaller build.spec --clean

# 3. El ejecutable estará en dist/DictadoPorVoz.exe
```

### Personalizar el Build

Edita `build.spec` para:
- Agregar icono: Descomenta `icon='assets/icon.ico'`
- Incluir archivos adicionales en `datas`
- Excluir módulos para reducir tamaño en `excludes`
- Cambiar de single-file a directory mode

---

## 📀 Crear el Instalador

### Prerrequisitos

1. **Tener el ejecutable compilado** (`dist/DictadoPorVoz.exe`)
2. **Inno Setup instalado** (https://jrsoftware.org/isdl.php)

### Compilar el Instalador

#### Opción 1: Interfaz Gráfica de Inno Setup

1. Abre **Inno Setup Compiler**
2. Menú: `File` → `Open...`
3. Selecciona: `installer.iss`
4. Menú: `Build` → `Compile`
5. Espera a que termine (~ 1 minuto)

**Resultado:** `output/DictadoPorVoz-Setup-v1.0.0.exe`

#### Opción 2: Línea de Comandos

```bash
# Compilar desde CMD
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss

# El instalador estará en: output/DictadoPorVoz-Setup-v1.0.0.exe
```

### Personalizar el Instalador

Edita `installer.iss` para:

```pascal
; Cambiar versión
#define MyAppVersion "1.0.0"  ; <-- Modificar aquí

; Cambiar información
#define MyAppPublisher "Tu Nombre"
#define MyAppURL "https://tu-sitio.com"

; Agregar icono (cuando lo tengas)
SetupIconFile=assets\icon.ico        ; Icono del instalador
UninstallDisplayIcon={app}\{#MyAppExeName}  ; Icono del desinstalador
```

---

## 📤 Distribución

### Qué Distribuir

Después del build exitoso, tienes DOS opciones:

#### Opción 1: Solo el Ejecutable (Portable)

**Archivo:** `dist/DictadoPorVoz.exe`

**Ventajas:**
- ✅ No requiere instalación
- ✅ Portable - puede copiarse a USB
- ✅ No toca el registro de Windows

**Cómo usar:**
1. Copiar `DictadoPorVoz.exe` donde quieras
2. Doble clic para ejecutar
3. Aparecerá en la bandeja del sistema

**Distribución:**
```bash
# Comprimir en ZIP
Compress-Archive -Path dist\DictadoPorVoz.exe -DestinationPath DictadoPorVoz-Portable-v1.0.0.zip
```

#### Opción 2: Instalador Completo

**Archivo:** `output/DictadoPorVoz-Setup-v1.0.0.exe`

**Ventajas:**
- ✅ Instalación profesional con asistente
- ✅ Acceso directo en Menú Inicio
- ✅ Desinstalador incluido
- ✅ Opción de auto-inicio con Windows
- ✅ Se registra en "Programas y características"

**Cómo usar:**
1. Ejecutar el instalador
2. Seguir el asistente
3. Elegir opciones:
   - ✓ Crear icono en escritorio
   - ✓ Iniciar con Windows (recomendado)
4. Finalizar instalación

### Tamaño de los Archivos

Tamaños aproximados:
- `DictadoPorVoz.exe`: ~80-120 MB
- `DictadoPorVoz-Setup-v1.0.0.exe`: ~85-125 MB

---

## 🎯 Proceso Completo de Build

### Workflow Recomendado

```bash
# 1. Preparación
cd dictado-por-voz-windows
git pull  # Si usas control de versiones

# 2. Actualizar dependencias
poetry install  # o pip install -r requirements-pyside6.txt

# 3. (Opcional) Agregar/actualizar icono
# Copiar icon.ico a assets/icon.ico

# 4. Compilar ejecutable
python build.py

# 5. Probar ejecutable
cd dist
.\DictadoPorVoz.exe
# Verificar que funciona correctamente
# Probar dictado, configuración, etc.

# 6. Crear instalador (si Inno Setup está instalado)
cd ..
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss

# 7. Probar instalador
cd output
.\DictadoPorVoz-Setup-v1.0.0.exe
# Instalar en una carpeta de prueba
```

### Checklist de Testing

Antes de distribuir, verificar:

- [ ] Ejecutable se inicia sin errores
- [ ] Icono aparece en bandeja del sistema
- [ ] Hotkey Ctrl+Shift+Space funciona
- [ ] Dictado funciona y escribe texto
- [ ] Menú de bandeja funciona
- [ ] Configuración rápida se abre
- [ ] Cambio de idioma funciona
- [ ] Auto-inicio con Windows funciona (si está activado)
- [ ] Notificaciones aparecen
- [ ] Instalador instala correctamente
- [ ] Desinstalador desinstala completamente

---

## 🚨 Solución de Problemas

### Error: "PyInstaller no encontrado"

```bash
# Solución:
pip install pyinstaller

# Verificar:
pyinstaller --version
```

### Error: "No module named 'PySide6'"

```bash
# Solución:
pip install PySide6

# O instalar todas las dependencias:
pip install -r requirements-pyside6.txt
```

### Error: "Failed to execute script"

**Causa:** Falta alguna dependencia o archivo

**Solución:**
1. Abrir `build.spec`
2. Agregar el módulo faltante en `hiddenimports`:
```python
hiddenimports=[
    'modulo_faltante',  # <-- Agregar aquí
    ...
]
```
3. Recompilar: `python build.py`

### Error: "Access Denied" al compilar

**Causa:** Archivo en uso o permisos

**Solución:**
1. Cerrar todas las instancias de la app
2. Ejecutar CMD como Administrador
3. Limpiar: `rmdir /s /q build dist`
4. Recompilar: `python build.py`

### El ejecutable es muy grande (>200 MB)

**Solución:** Optimizar el build

1. Editar `build.spec`
2. Agregar más exclusiones:
```python
excludes=[
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
    'tkinter',
    'unittest',  # <-- Agregar más aquí
    'test',
],
```
3. Habilitar UPX compression:
```python
upx=True,  # Compresión UPX
```

### Instalador no se puede compilar

**Error:** "Cannot find Inno Setup"

**Solución:**
1. Instalar Inno Setup: https://jrsoftware.org/isdl.php
2. Agregar a PATH o usar ruta completa:
```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

### Error: "icon.ico not found"

**Solución temporal:** Comentar las líneas de icono

En `build.spec`:
```python
# icon='assets/icon.ico',  # <-- Comentar
```

En `installer.iss`:
```pascal
; SetupIconFile=assets\icon.ico  ; <-- Comentar
```

---

## 📝 Notas Adicionales

### Versionado

Cuando actualices la versión:

1. Actualizar `installer.iss`:
```pascal
#define MyAppVersion "1.1.0"  ; <-- Nueva versión
```

2. Actualizar `build.py` si tiene información de versión

3. Crear tag en git:
```bash
git tag -a v1.1.0 -m "Version 1.1.0"
git push origin v1.1.0
```

### Firma de Código (Code Signing)

Para producción, considera firmar el ejecutable:

1. Obtener certificado de firma de código
2. Usar `signtool.exe` de Windows SDK:
```bash
signtool sign /f certificate.pfx /p password /t http://timestamp.server dist\DictadoPorVoz.exe
```

### Continuous Integration

Para automatizar el build con GitHub Actions, CI/CD, etc.:

1. Crear workflow que ejecute `python build.py`
2. Subir artifacts (ejecutable e instalador)
3. Crear release automáticamente

---

## 🎉 ¡Listo para Distribuir!

Ahora tienes:
- ✅ `dist/DictadoPorVoz.exe` - Ejecutable portable
- ✅ `output/DictadoPorVoz-Setup-v1.0.0.exe` - Instalador completo
- ✅ Listo para compartir con usuarios

### Compartir

- **GitHub Releases:** Sube los archivos como release
- **Google Drive / Dropbox:** Comparte enlaces
- **Sitio web:** Descarga directa
- **Microsoft Store:** Empaqueta como MSIX (avanzado)

---

**Desarrollado por Gyno Romero Prado**
**Licencia: MIT**
