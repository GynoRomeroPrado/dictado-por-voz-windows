import os
import urllib.request

def download_model():
    assets_dir = os.path.join("src", "assets")
    os.makedirs(assets_dir, exist_ok=True)
    target_path = os.path.join(assets_dir, "silero_vad.onnx")

    urls = [
        "https://github.com/snakers4/silero-vad/raw/master/files/silero_vad.onnx",
        "https://github.com/snakers4/silero-vad/raw/main/files/silero_vad.onnx",
        "https://github.com/snakers4/silero-vad/raw/v4.0/files/silero_vad.onnx",
        "https://raw.githubusercontent.com/snakers4/silero-vad/master/files/silero_vad.onnx"
    ]
    
    for url in urls:
        print(f"Trying {url}...")
        try:
            urllib.request.urlretrieve(url, target_path)
            if os.path.exists(target_path) and os.path.getsize(target_path) > 1000:
                print("Download complete!")
                return
        except Exception as e:
            print(f"Failed: {e}")
            
    print("All downloads failed.")

if __name__ == "__main__":
    download_model()
