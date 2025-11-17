# Guía de Instalación - Dictado por Voz Windows

Esta guía te ayudará a instalar y configurar la aplicación de dictado por voz en tu sistema Windows.

## Requisitos del Sistema

### Sistema Operativo
- Windows 10 (build 1809 o superior)
- Windows 11

### Software Requerido
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Micrófono funcional

### Espacio en Disco
- Aproximadamente 500 MB de espacio libre

## Instalación Paso a Paso

### 1. Instalar Python

Si no tienes Python instalado:

1. Descarga Python desde [python.org](https://www.python.org/downloads/)
2. Ejecuta el instalador
3. **IMPORTANTE**: Marca la casilla "Add Python to PATH"
4. Haz clic en "Install Now"

Verifica la instalación abriendo PowerShell o CMD:
```bash
python --version
pip --version
```

### 2. Clonar o Descargar el Repositorio

**Opción A: Con Git**
```bash
git clone https://github.com/GynoRomeroPrado/dictado-por-voz-windows.git
cd dictado-por-voz-windows
```

**Opción B: Descarga Manual**
1. Ve a la página del repositorio en GitHub
2. Haz clic en "Code" → "Download ZIP"
3. Extrae el archivo ZIP
4. Abre PowerShell/CMD en la carpeta extraída

### 3. Crear Entorno Virtual (Recomendado)

```bash
python -m venv venv
```

Activar el entorno virtual:
```bash
# En PowerShell
.\venv\Scripts\Activate.ps1

# En CMD
.\venv\Scripts\activate.bat
```

Si aparece un error de permisos en PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Nota sobre PyAudio**: Si tienes problemas instalando PyAudio:

1. Descarga el wheel apropiado desde [aquí](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
2. Instala manualmente:
   ```bash
   pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl
   ```
   (Ajusta el nombre del archivo según tu versión de Python)

### 5. Configurar Permisos del Micrófono

1. Ve a **Configuración de Windows** → **Privacidad**
2. Selecciona **Micrófono** en el menú lateral
3. Asegúrate de que:
   - "Permitir que las aplicaciones accedan al micrófono" esté **Activado**
   - Python tenga permiso para acceder al micrófono

### 6. Configurar Windows Speech Recognition (Opcional pero Recomendado)

Para mejor precisión con el motor de Windows:

1. Ve a **Panel de Control** → **Accesibilidad** → **Reconocimiento de voz**
2. Haz clic en "Iniciar el reconocimiento de voz"
3. Sigue el asistente para:
   - Configurar tu micrófono
   - Entrenar el reconocimiento de voz (recomendado)
   - Seleccionar tu idioma

### 7. Ejecutar la Aplicación

```bash
python src/main.py
```

O si instalaste el paquete:
```bash
dictado-voz
```

## Solución de Problemas Comunes

### Error: "No module named 'PyQt5'"
```bash
pip install PyQt5
```

### Error: "No module named 'speech_recognition'"
```bash
pip install SpeechRecognition
```

### Error: PyAudio no se instala
Descarga el wheel precompilado:
```bash
pip install pipwin
pipwin install pyaudio
```

### Error: "Access denied" al registrar hotkeys
- Ejecuta PowerShell/CMD como Administrador
- Verifica que no haya otra aplicación usando los mismos atajos

### El micrófono no funciona
1. Verifica que el micrófono esté conectado
2. Prueba el micrófono en otras aplicaciones
3. Revisa los permisos de privacidad de Windows
4. Ejecuta el test de micrófono:
   ```python
   python -c "from src.core.speech_recognizer import SpeechRecognizer; sr = SpeechRecognizer(); print('OK' if sr.test_microphone() else 'FAIL')"
   ```

### Problema: Reconocimiento impreciso
1. Entrena Windows Speech Recognition (ver paso 6)
2. Ajusta el "Umbral de energía" en Configuración
3. Reduce el ruido ambiental
4. Habla más cerca del micrófono
5. Cambia el motor de reconocimiento en Configuración

## Configuración Inicial

Al ejecutar por primera vez:

1. La aplicación creará los archivos de configuración en `config/`
2. Revisa y ajusta `config/settings.json` según tus preferencias
3. Personaliza comandos en `config/commands.json`

### Configuración Recomendada para Español

En `config/settings.json`:
```json
{
  "language": "es-ES",
  "recognition": {
    "engine": "google",
    "confidence_threshold": 0.7
  }
}
```

## Actualización

Para actualizar a la última versión:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## Desinstalación

1. Cierra la aplicación
2. Desactiva el entorno virtual: `deactivate`
3. Elimina la carpeta del proyecto
4. (Opcional) Desinstala Python si no lo necesitas

## Próximos Pasos

1. Lee el [README.md](README.md) para conocer las características
2. Revisa los comandos de voz predefinidos
3. Personaliza tus comandos en `config/commands.json`
4. Configura tus atajos de teclado preferidos

## Soporte

Si encuentras problemas:
- Revisa los [Issues en GitHub](https://github.com/GynoRomeroPrado/dictado-por-voz-windows/issues)
- Crea un nuevo issue con detalles del error
- Incluye el archivo de log si está disponible
