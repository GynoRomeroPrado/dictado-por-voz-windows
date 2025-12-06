import sys
import os
import time

def step(name):
    print(f"\n[{name}]")
    print("-" * 40)

def test_whisper_import():
    step("Testing faster-whisper Import")
    print(f"Python Executable: {sys.executable}")
    print(f"Python Version: {sys.version}")
    
    try:
        import faster_whisper
        print(f"SUCCESS: faster_whisper imported. Version: {faster_whisper.__version__}")
        return True
    except ImportError as e:
        print(f"FAILURE: Could not import faster_whisper: {e}")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_whisper_model():
    step("Testing Whisper Model Loading")
    try:
        from faster_whisper import WhisperModel
        print("Loading WhisperModel ('base', cpu, int8)...")
        start = time.time()
        # Ensure we don't download if not needed, or verify download works
        model = WhisperModel("base", device="cpu", compute_type="int8")
        print(f"SUCCESS: Model loaded in {time.time() - start:.2f}s")
        return True
    except Exception as e:
        print(f"FAILURE: Model loading failed: {e}")
        return False

if __name__ == "__main__":
    if test_whisper_import():
        test_whisper_model()
