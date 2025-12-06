
try:
    print("Importing faster_whisper...")
    from faster_whisper import WhisperModel
    print("Success!")
    
    print("Attempting to load model (base)...")
    # Try to load/download model
    model = WhisperModel("base", device="cpu", compute_type="int8")
    print("Model loaded successfully!")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
