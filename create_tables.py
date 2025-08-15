#!/usr/bin/env python3
"""
Script para crear las tablas de la base de datos.
Ejecutar desde la raíz del proyecto: python create_tables.py
"""

from main import create_app
from src.config.extensions import db
from src.models.user import User, Role, TokenBlocklist

def create_tables():
    """Crear todas las tablas de la base de datos."""
    app = create_app()
    
    with app.app_context():
        try:
            db.create_all()
            print("✅ Tablas creadas exitosamente.")
            
            # Verificar que las tablas se crearon
            tables = db.engine.table_names()
            print(f"📋 Tablas creadas: {', '.join(tables)}")
            
        except Exception as e:
            print(f"❌ Error al crear las tablas: {e}")
            return False
    
    return True

if __name__ == "__main__":
    create_tables()
