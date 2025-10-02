"""
Script de migración para agregar las tablas de indexación
"""
from database.database import engine
import database.models as models

def migrate_indexing_tables():
    """Crea las nuevas tablas de indexación"""
    print("Creating indexing tables...")
    
    # Crear solo las nuevas tablas
    models.IndexedFile.__table__.create(engine, checkfirst=True)
    models.IndexingJob.__table__.create(engine, checkfirst=True)
    
    print("Indexing tables created successfully!")

if __name__ == "__main__":
    migrate_indexing_tables()
