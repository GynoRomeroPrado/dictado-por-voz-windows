import sys
import os
import time
import numpy as np

# Add src to path
sys.path.insert(0, os.path.abspath('src'))

def test_whisper():
    print("Testing Whisper Local...")
    try:
        from faster_whisper import WhisperModel
        print("faster_whisper imported successfully.")
        
        print("Loading model 'base' on CPU (int8)...")
        start = time.time()
        model = WhisperModel("base", device="cpu", compute_type="int8")
        print(f"Model loaded in {time.time() - start:.2f} seconds.")
        
        # Test transcription with silence or dummy audio
        # Create 1 second of silence/noise
        print("Generating dummy audio...")
        dummy_audio = np.zeros(16000, dtype=np.float32)
        
        print("Transcribing dummy audio...")
        segments, info = model.transcribe(dummy_audio, beam_size=5)
        
        text = " ".join([segment.text for segment in segments]).strip()
        print(f"Transcription result: '{text}'")
        print("Whisper test complete.")
        
    except Exception as e:
        print(f"CRITICAL ERROR in Whisper: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_whisper()
