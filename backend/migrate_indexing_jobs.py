#!/usr/bin/env python3
"""
Migration script to update IndexingJob table structure
- Add missing columns for job queue functionality
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
    """Run the migration to update IndexingJob table"""
    
    # Get database URL
    database_url = SQLALCHEMY_DATABASE_URL
    engine = create_engine(database_url)
    
    try:
        with engine.connect() as conn:
            # Start transaction
            trans = conn.begin()
            
            try:
                logger.info("Starting IndexingJob table migration...")
                
                # Step 1: Add missing columns
                logger.info("Adding missing columns...")
                
                new_columns = [
                    "ALTER TABLE indexing_jobs ADD COLUMN IF NOT EXISTS priority INTEGER DEFAULT 0;",
                    "ALTER TABLE indexing_jobs ADD COLUMN IF NOT EXISTS retry_count INTEGER DEFAULT 0;",
                    "ALTER TABLE indexing_jobs ADD COLUMN IF NOT EXISTS max_retries INTEGER DEFAULT 3;",
                    "ALTER TABLE indexing_jobs ADD COLUMN IF NOT EXISTS scheduled_at TIMESTAMP WITH TIME ZONE;",
                    "ALTER TABLE indexing_jobs ADD COLUMN IF NOT EXISTS locked_at TIMESTAMP WITH TIME ZONE;",
                    "ALTER TABLE indexing_jobs ADD COLUMN IF NOT EXISTS locked_by VARCHAR;",
                    "ALTER TABLE indexing_jobs ADD COLUMN IF NOT EXISTS total_files INTEGER DEFAULT 0;",
                    "ALTER TABLE indexing_jobs ADD COLUMN IF NOT EXISTS processed_files INTEGER DEFAULT 0;",
                    "ALTER TABLE indexing_jobs ADD COLUMN IF NOT EXISTS successful_files INTEGER DEFAULT 0;",
                    "ALTER TABLE indexing_jobs ADD COLUMN IF NOT EXISTS failed_files INTEGER DEFAULT 0;",
                    "ALTER TABLE indexing_jobs ADD COLUMN IF NOT EXISTS error_message TEXT;",
                    "ALTER TABLE indexing_jobs ADD COLUMN IF NOT EXISTS started_at TIMESTAMP WITH TIME ZONE;",
                    "ALTER TABLE indexing_jobs ADD COLUMN IF NOT EXISTS completed_at TIMESTAMP WITH TIME ZONE;",
                    "ALTER TABLE indexing_jobs ADD COLUMN IF NOT EXISTS job_parameters TEXT;"
                ]
                
                for sql in new_columns:
                    try:
                        conn.execute(text(sql))
                        logger.info(f"✓ Executed: {sql}")
                    except Exception as e:
                        if "already exists" in str(e).lower() or "duplicate column" in str(e).lower():
                            logger.info(f"✓ Column already exists: {sql}")
                        else:
                            logger.warning(f"⚠ Error adding column: {e}")
                
                # Step 2: Create indexes
                logger.info("Creating indexes...")
                
                indexes = [
                    "CREATE INDEX IF NOT EXISTS idx_indexing_jobs_priority ON indexing_jobs(priority);",
                    "CREATE INDEX IF NOT EXISTS idx_indexing_jobs_status ON indexing_jobs(status);",
                    "CREATE INDEX IF NOT EXISTS idx_indexing_jobs_scheduled_at ON indexing_jobs(scheduled_at);"
                ]
                
                for sql in indexes:
                    try:
                        conn.execute(text(sql))
                        logger.info(f"✓ Executed: {sql}")
                    except Exception as e:
                        if "already exists" in str(e).lower():
                            logger.info(f"✓ Index already exists: {sql}")
                        else:
                            logger.warning(f"⚠ Error creating index: {e}")
                
                # Commit transaction
                trans.commit()
                logger.info("✅ IndexingJob migration completed successfully!")
                
            except Exception as e:
                trans.rollback()
                logger.error(f"❌ Migration failed: {e}")
                raise
                
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        raise

if __name__ == "__main__":
    run_migration()
