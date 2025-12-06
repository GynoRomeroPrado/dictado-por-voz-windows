import sys
import os
import speech_recognition as sr
import numpy as np

# Add src to path
sys.path.insert(0, os.path.abspath('src'))

def test_google():
    print("Testing Google Speech Recognition...")
    recognizer = sr.Recognizer()
    
    # Simulate audio data (or record if possible, but simulation is safer for automated test)
    # Actually, recognize_google requires valid FLAC/WAV data. Empty/dummy noise might result in "UnknownValueError".
    
    # Let's try to interpret "silence" - it should raise UnknownValueError
    # But to test if the API is typically reachable, we might need real audio.
    
    # We can create a sine wave (beep) that sounds like "a"? No that's hard.
    
    # Let's just check if we can call the method without import errors.
    try:
        # Create dummy audio data
        # 16000 Hz, 2 bytes, 1 second mono
        dummy_audio_bytes = b'\x00' * 32000 
        audio = sr.AudioData(dummy_audio_bytes, 16000, 2)
        
        print("Sending dummy silent audio to Google...")
        try:
            recognizer.recognize_google(audio, language="es-MX")
        except sr.UnknownValueError:
            print("Google API reached (returned UnknownValueError for silence). Success!")
        except sr.RequestError as e:
            print(f"Google API reachable but returned error: {e}")
            
    except Exception as e:
        print(f"CRITICAL ERROR testing Google SR: {e}")

if __name__ == "__main__":
    test_google()
