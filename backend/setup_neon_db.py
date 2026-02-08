#!/usr/bin/env python3
"""
Script to setup database tables in Neon database
"""

import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine
from models.user import User
from models.todo import Todo, TodoStatus

# Load environment variables from .env file
load_dotenv(dotenv_path="../.env")  # Try parent directory first
if not os.getenv("DATABASE_URL"):
    load_dotenv()  # Try current directory


def setup_database():
    """
    Create database tables in Neon database
    """
    # Get the Neon database URL from environment
    database_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://username:password@localhost/dbname")
    print(f"Connecting to database: {database_url}")
    
    # Convert async URL to sync URL for table creation
    sync_database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")
    
    # Create sync engine for table creation
    sync_engine = create_engine(sync_database_url)
    
    # Create all tables
    SQLModel.metadata.create_all(sync_engine)
    
    print("Database tables created successfully!")
    
    # Print table information
    from sqlalchemy import inspect
    inspector = inspect(sync_engine)
    
    for table_name in inspector.get_table_names():
        print(f"\nTable: {table_name}")
        columns = inspector.get_columns(table_name)
        for col in columns:
            pk_flag = "[PK]" if col.get('primary_key', False) else ""
            null_flag = "[NULL]" if col.get('nullable', True) else "[NOT NULL]"
            print(f"  - {col['name']} ({col['type']}) {pk_flag} {null_flag}")


if __name__ == "__main__":
    setup_database()