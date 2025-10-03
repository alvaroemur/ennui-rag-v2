#!/usr/bin/env python3
"""
Migration script to update IndexedFile table structure
- Add new Google API parameters
- Add enrichment columns
- Remove deprecated columns
- Change program_id to drive_folder_id
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from database.database import SQLALCHEMY_DATABASE_URL
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migration():
    """Run the migration to update IndexedFile table"""
    
    # Get database URL
    database_url = SQLALCHEMY_DATABASE_URL
    engine = create_engine(database_url)
    
    try:
        with engine.connect() as conn:
            # Start transaction
            trans = conn.begin()
            
            try:
                logger.info("Starting IndexedFile table migration...")
                
                # Step 1: Add new columns
                logger.info("Adding new columns...")
                
                new_columns = [
                    "ALTER TABLE indexed_files ADD COLUMN drive_folder_id VARCHAR;",
                    "ALTER TABLE indexed_files ADD COLUMN description TEXT;",
                    "ALTER TABLE indexed_files ADD COLUMN parents TEXT;",
                    "ALTER TABLE indexed_files ADD COLUMN owners TEXT;",
                    "ALTER TABLE indexed_files ADD COLUMN last_modifying_user TEXT;",
                    "ALTER TABLE indexed_files ADD COLUMN md5_checksum VARCHAR;",
                    "ALTER TABLE indexed_files ADD COLUMN summary_120w TEXT;",
                    "ALTER TABLE indexed_files ADD COLUMN keywords TEXT;",
                    "ALTER TABLE indexed_files ADD COLUMN topics TEXT;",
                    "ALTER TABLE indexed_files ADD COLUMN sentiment VARCHAR;",
                    "ALTER TABLE indexed_files ADD COLUMN language VARCHAR;",
                    "ALTER TABLE indexed_files ADD COLUMN document_type VARCHAR;"
                ]
                
                for sql in new_columns:
                    try:
                        conn.execute(text(sql))
                        logger.info(f"✓ Executed: {sql}")
                    except Exception as e:
                        if "already exists" in str(e).lower():
                            logger.info(f"✓ Column already exists: {sql}")
                        else:
                            logger.warning(f"⚠ Error adding column: {e}")
                
                # Step 2: Populate drive_folder_id from programs table
                logger.info("Populating drive_folder_id from programs table...")
                update_sql = """
                UPDATE indexed_files 
                SET drive_folder_id = (
                    SELECT drive_folder_id 
                    FROM programs 
                    WHERE programs.id = indexed_files.program_id
                )
                WHERE program_id IS NOT NULL;
                """
                
                result = conn.execute(text(update_sql))
                logger.info(f"✓ Updated {result.rowcount} records with drive_folder_id")
                
                # Step 3: Create index on drive_folder_id
                logger.info("Creating index on drive_folder_id...")
                try:
                    conn.execute(text("CREATE INDEX idx_indexed_files_drive_folder_id ON indexed_files(drive_folder_id);"))
                    logger.info("✓ Created index on drive_folder_id")
                except Exception as e:
                    if "already exists" in str(e).lower():
                        logger.info("✓ Index on drive_folder_id already exists")
                    else:
                        logger.warning(f"⚠ Error creating index: {e}")
                
                # Step 4: Remove old columns
                logger.info("Removing deprecated columns...")
                
                deprecated_columns = [
                    "program_id",
                    "mime_type", 
                    "drive_file_path",
                    "content_hash"
                ]
                
                for column in deprecated_columns:
                    try:
                        conn.execute(text(f"ALTER TABLE indexed_files DROP COLUMN {column};"))
                        logger.info(f"✓ Removed column: {column}")
                    except Exception as e:
                        if "does not exist" in str(e).lower():
                            logger.info(f"✓ Column {column} already removed")
                        else:
                            logger.warning(f"⚠ Error removing column {column}: {e}")
                
                # Step 5: Make drive_folder_id NOT NULL
                logger.info("Making drive_folder_id NOT NULL...")
                try:
                    conn.execute(text("ALTER TABLE indexed_files ALTER COLUMN drive_folder_id SET NOT NULL;"))
                    logger.info("✓ Made drive_folder_id NOT NULL")
                except Exception as e:
                    logger.warning(f"⚠ Error making drive_folder_id NOT NULL: {e}")
                
                # Commit transaction
                trans.commit()
                logger.info("✅ Migration completed successfully!")
                
            except Exception as e:
                trans.rollback()
                logger.error(f"❌ Migration failed: {e}")
                raise
                
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        raise

if __name__ == "__main__":
    run_migration()
