#!/usr/bin/env python
"""
Punto de entrada para la versión SIMPLIFICADA de Dictado por Voz
Solo icono en bandeja + hotkey global + escritura directa

USO:
  python run_simple.py

CARACTERÍSTICAS:
  - No ventana principal, solo icono en bandeja
  - Presiona Ctrl+Shift+Space para iniciar dictado
  - Habla y el texto se escribe donde está el cursor
  - Funciona en CUALQUIER aplicación de Windows
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run main
if __name__ == "__main__":
    try:
        from main_simple import main
        main()
    except KeyboardInterrupt:
        print("\nAplicación interrumpida por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error al iniciar la aplicación: {e}")
        print("\nAsegúrate de que todas las dependencias están instaladas:")
        print("  poetry install")
        print("  o")
        print("  pip install -r requirements.txt")
        print("\nEn Windows, es posible que necesites ejecutar como administrador")
        print("para que los hotkeys globales funcionen correctamente.")
        sys.exit(1)
