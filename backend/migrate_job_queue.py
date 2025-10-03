#!/usr/bin/env python3
"""
Migration script to add job queue fields to IndexingJob table
"""
import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def migrate_job_queue():
    """Add job queue fields to IndexingJob table"""
    
    # Get database URL from environment
    database_url = os.getenv("SQLALCHEMY_DATABASE_URL")
    if not database_url:
        print("❌ SQLALCHEMY_DATABASE_URL environment variable not set")
        sys.exit(1)
    
    engine = create_engine(database_url)
    
    # SQL statements to add new columns
    migration_sql = [
        # Add priority column
        "ALTER TABLE indexing_jobs ADD COLUMN IF NOT EXISTS priority INTEGER DEFAULT 0;",
        
        # Add retry_count column
        "ALTER TABLE indexing_jobs ADD COLUMN IF NOT EXISTS retry_count INTEGER DEFAULT 0;",
        
        # Add max_retries column
        "ALTER TABLE indexing_jobs ADD COLUMN IF NOT EXISTS max_retries INTEGER DEFAULT 3;",
        
        # Add scheduled_at column
        "ALTER TABLE indexing_jobs ADD COLUMN IF NOT EXISTS scheduled_at TIMESTAMP WITH TIME ZONE;",
        
        # Add locked_at column
        "ALTER TABLE indexing_jobs ADD COLUMN IF NOT EXISTS locked_at TIMESTAMP WITH TIME ZONE;",
        
        # Add locked_by column
        "ALTER TABLE indexing_jobs ADD COLUMN IF NOT EXISTS locked_by VARCHAR;",
        
        # Add job_parameters column
        "ALTER TABLE indexing_jobs ADD COLUMN IF NOT EXISTS job_parameters TEXT;",
        
        # Create indexes for better performance
        "CREATE INDEX IF NOT EXISTS idx_indexing_jobs_priority ON indexing_jobs(priority);",
        "CREATE INDEX IF NOT EXISTS idx_indexing_jobs_scheduled_at ON indexing_jobs(scheduled_at);",
        "CREATE INDEX IF NOT EXISTS idx_indexing_jobs_locked_by ON indexing_jobs(locked_by);",
    ]
    
    try:
        with engine.begin() as connection:
            print("Starting job queue migration...")
            
            for i, sql in enumerate(migration_sql, 1):
                print(f"Executing migration step {i}/{len(migration_sql)}: {sql[:50]}...")
                connection.execute(text(sql))
            
            print("✅ Job queue migration completed successfully!")
            
            # Verify the migration
            result = connection.execute(text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'indexing_jobs' 
                AND column_name IN ('priority', 'retry_count', 'max_retries', 'scheduled_at', 'locked_at', 'locked_by', 'job_parameters')
                ORDER BY column_name;
            """))
            
            print("\nVerification - New columns added:")
            for row in result:
                print(f"  {row[0]}: {row[1]} (nullable: {row[2]}, default: {row[3]})")
            
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    migrate_job_queue()
