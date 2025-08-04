#!/usr/bin/env python3
"""
Sistema de Gestión de Stock y Ventas de Artículos Elétricos e Iluminación
Estructura MVC - Versión refactorizada
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from views.main_window import MainWindow
from db.database import db

def main():
    """Función principal de la aplicación"""
    try:
        # Inicializar base de datos
        print("Inicializando base de datos...")
        db.create_tables()
        print("✅ Base de datos inicializada")
        
        # Crear y ejecutar aplicación
        print("Iniciando aplicación...")
        app = MainWindow()
        print("✅ Aplicación iniciada")
        
        app.run()
        
    except Exception as e:
        print(f"❌ Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()