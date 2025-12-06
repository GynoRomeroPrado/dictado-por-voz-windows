import sys
import os
import time
import numpy as np

# Add src to path
sys.path.insert(0, os.path.abspath('src'))

def step(name):
    print(f"\n[{name}]")
    print("-" * 40)

def test_keyboard_module():
    step("Testing keyboard module")
    try:
        import keyboard
        print(f"KEYBOARD MODULE FOUND: {keyboard}")
        return True
    except ImportError:
        print("CRITICAL: keyboard module NOT FOUND")
        return False

def test_clipboard_manager():
    step("Testing ClipboardManager")
    try:
        from utils.clipboard import ClipboardManager
        
        print("Testing type_text (Writing 'test_type' in 3 seconds...)")
        print("Please place cursor in a text field!")
        time.sleep(3)
        success = ClipboardManager.type_text("test_type ")
        print(f"type_text result: {success}")
        
        print("Testing insert_text (Pasting 'test_paste' in 3 seconds...)")
        time.sleep(2)
        success = ClipboardManager.insert_text("test_paste ")
        print(f"insert_text result: {success}")
        
    except Exception as e:
        print(f"Error testing ClipboardManager: {e}")

def test_microphone_levels():
    step("Testing Microphone Levels")
    try:
        import sounddevice as sd
        from utils.config import config
        
        energy_threshold = config.get('recognition.energy_threshold', 600)
        print(f"Configured Energy Threshold: {energy_threshold}")
        
        duration = 5 # seconds
        fs = 16000
        
        print(f"Recording for {duration} seconds. Please speak normally...")
        
        def callback(indata, frames, time, status):
            if status:
                print(status)
            rms = np.sqrt(np.mean(indata.flatten().astype(np.float64)**2))
            print(f"RMS: {int(rms)} | Threshold: {energy_threshold} | {'SPEECH' if rms > energy_threshold else 'Silence'}")
            
        with sd.InputStream(callback=callback, channels=1, samplerate=fs, dtype='int16'):
            sd.sleep(duration * 1000)
            
    except Exception as e:
        print(f"Error testing microphone: {e}")

def main():
    if test_keyboard_module():
        test_clipboard_manager()
    
    test_microphone_levels()

if __name__ == "__main__":
    main()
