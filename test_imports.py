
try:
    import PyInstaller
    print("PyInstaller: OK")
except ImportError as e:
    print(f"PyInstaller: FAIL ({e})")

try:
    import speech_recognition
    print("speech_recognition: OK")
except ImportError as e:
    print(f"speech_recognition: FAIL ({e})")

try:
    import PySide6
    print("PySide6: OK")
except ImportError as e:
    print(f"PySide6: FAIL ({e})")
