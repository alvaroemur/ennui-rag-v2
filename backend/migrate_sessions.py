#!/usr/bin/env python3
"""
Migration script to add UserSession table to the database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import engine, Base
from database.models import UserSession

def migrate_sessions():
    """Create the user_sessions table"""
    try:
        # Create the table
        UserSession.__table__.create(engine, checkfirst=True)
        print("✅ UserSession table created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating UserSession table: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Creating UserSession table...")
    success = migrate_sessions()
    if success:
        print("✅ Migration completed successfully")
    else:
        print("❌ Migration failed")
        sys.exit(1)

