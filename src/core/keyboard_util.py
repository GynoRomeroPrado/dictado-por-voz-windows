import keyboard
import time

class KeyboardInjector:
    @staticmethod
    def type_text(text):
        if not text:
            return

        # Smart Spacing: Añadir espacio inicial si es necesario
        # (Esto es difícil de saber sin contexto del portapapeles, 
        #  pero asumiremos que un dictado continuo necesita espacio previo 
        #  si no es el inicio absoluto)
        
        try:
            print(f"DEBUG: [Keyboard] Injecting text: '{text}'")
            # Opción 1: Write directo (más compatible con juegos/apps raras)
            keyboard.write(" " + text)
            print("DEBUG: [Keyboard] Text injected.")
            
        except Exception as e:
            print(f"Error inyectando texto: {e}")
