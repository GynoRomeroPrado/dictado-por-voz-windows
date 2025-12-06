# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller build specification for Dictado por Voz Windows
Generates a single-file executable with all dependencies bundled
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all PySide6 data files
pyside6_datas = collect_data_files('PySide6')

# Collect all speech_recognition data files
speech_datas = collect_data_files('speech_recognition')

block_cipher = None

a = Analysis(
    ['run_simple.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Include config directory
        ('config', 'config'),
        # Include PySide6 data files
        *pyside6_datas,
        # Include speech_recognition data
        *speech_datas,
    ],
    hiddenimports=[
        # PySide6 modules
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        # Speech recognition
        'speech_recognition',
        'pyaudio',
        # Keyboard and clipboard
        'keyboard',
        'pyperclip',
        # Windows specific
        'win32api',
        'win32con',
        'win32gui',
        'winreg',
        'winsound',
        # Application modules
        'src.main_simple',
        'src.gui.tray_icon',
        'src.gui.settings_dialog',
        'src.gui.quick_settings',
        'src.core.speech_recognizer',
        'src.core.command_processor',
        'src.core.hotkey_manager',
        'src.core.clipboard_manager',
        'src.utils.config',
        'src.utils.auto_start',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'matplotlib', 'PyQt5',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DictadoPorVoz',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # No console window (Windows GUI app)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='assets/icon.ico',  # Uncomment when icon is available
    version_file=None,  # Can add version info later
)
