#!/usr/bin/env python
"""
Build script for Dictado por Voz - Windows

This script automates the build process:
1. Checks dependencies
2. Runs PyInstaller
3. Creates distribution folder
4. Generates installer (if Inno Setup is available)

Usage:
    python build.py
    python build.py --clean  # Clean build artifacts first
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def print_step(step_num, total, text):
    """Print a step indicator"""
    print(f"\n[{step_num}/{total}] {text}...")


def check_dependencies():
    """Check if all required dependencies are installed"""
    print_step(1, 4, "Verificando dependencias")

    required = {
        'PyInstaller': 'pyinstaller',
        'PySide6': 'PySide6',
        'SpeechRecognition': 'speech_recognition',
    }

    missing = []
    for name, module in required.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} (falta)")
            missing.append(name)

    if missing:
        print("\n❌ Faltan dependencias:")
        print("   Ejecuta: pip install -r requirements-pyside6.txt")
        print("   O:       poetry install")
        return False

    print("\n✓ Todas las dependencias están instaladas")
    return True


def clean_build():
    """Clean previous build artifacts"""
    print_step(2, 4, "Limpiando archivos anteriores")

    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec']

    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  ✓ Eliminado: {dir_name}/")

    for pattern in files_to_clean:
        for file in Path('.').glob(pattern):
            if file.name != 'build.spec':  # Keep our custom spec
                file.unlink()
                print(f"  ✓ Eliminado: {file}")

    print("✓ Limpieza completada")


def run_pyinstaller():
    """Run PyInstaller to create the executable"""
    print_step(3, 4, "Compilando con PyInstaller")

    try:
        # Run PyInstaller with the build.spec file
        cmd = [sys.executable, '-m', 'PyInstaller', 'build.spec', '--clean']

        print("  Ejecutando:", ' '.join(cmd))
        print("  (Esto puede tardar varios minutos...)\n")

        result = subprocess.run(
            cmd,
            check=True,
            capture_output=False,  # Show output in real-time
            text=True
        )

        print("\n✓ Compilación exitosa")
        return True

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error durante la compilación: {e}")
        return False
    except FileNotFoundError:
        print("\n❌ PyInstaller no encontrado")
        print("   Ejecuta: pip install pyinstaller")
        return False


def create_distribution():
    """Create distribution folder with necessary files"""
    print_step(4, 4, "Creando carpeta de distribución")

    dist_dir = Path('dist')
    exe_path = dist_dir / 'DictadoPorVoz.exe'

    if not exe_path.exists():
        print(f"❌ No se encontró el ejecutable: {exe_path}")
        return False

    # Create config directory in dist if needed
    config_dist = dist_dir / 'config'
    if not config_dist.exists():
        config_src = Path('config')
        if config_src.exists():
            shutil.copytree(config_src, config_dist)
            print(f"  ✓ Copiada carpeta de configuración")

    # Copy README
    readme_src = Path('README_SIMPLE.md')
    readme_dist = dist_dir / 'README.txt'
    if readme_src.exists():
        shutil.copy2(readme_src, readme_dist)
        print(f"  ✓ Copiado README")

    # Create version info file
    version_file = dist_dir / 'VERSION.txt'
    with open(version_file, 'w', encoding='utf-8') as f:
        f.write("Dictado por Voz para Windows\n")
        f.write("Versión: 1.0.0\n")
        f.write("Desarrollador: Gyno Romero Prado\n")
    print(f"  ✓ Creado archivo de versión")

    print(f"\n✓ Distribución creada en: {dist_dir.absolute()}")
    print(f"✓ Ejecutable: {exe_path.absolute()}")

    return True


def main():
    """Main build process"""
    print_header("🔨 BUILD - DICTADO POR VOZ PARA WINDOWS")

    # Check for --clean flag
    if '--clean' in sys.argv:
        clean_build()

    # Step 1: Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Step 2: Clean (if not already done)
    if '--clean' not in sys.argv:
        clean_build()

    # Step 3: Run PyInstaller
    if not run_pyinstaller():
        sys.exit(1)

    # Step 4: Create distribution
    if not create_distribution():
        sys.exit(1)

    # Success!
    print_header("✅ BUILD COMPLETADO EXITOSAMENTE")
    print("El ejecutable está listo para usar:")
    print(f"  📁 dist/DictadoPorVoz.exe")
    print("\nPara crear un instalador:")
    print("  1. Instala Inno Setup: https://jrsoftware.org/isdl.php")
    print("  2. Ejecuta: iscc installer.iss")
    print("\nPara probar el ejecutable:")
    print("  cd dist")
    print("  .\\DictadoPorVoz.exe")


if __name__ == "__main__":
    main()
