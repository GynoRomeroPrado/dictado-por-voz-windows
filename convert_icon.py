"""
Script para convertir PNG a ICO con el nuevo icono oscuro
"""
from PIL import Image

# Convertir nuevo PNG oscuro a ICO
png_path = r"C:\Users\GYNO\.gemini\antigravity\brain\edbfd754-cad5-4950-8fd6-67387af72d4b\app_icon_dark_1765485916519.png"
ico_path = r"g:\dictado-por-voz-windows-1\src\assets\app_icon.ico"

img = Image.open(png_path)
# Convertir RGBA si es necesario
if img.mode != 'RGBA':
    img = img.convert('RGBA')

img.save(ico_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
print(f"Icono OSCURO guardado en: {ico_path}")
