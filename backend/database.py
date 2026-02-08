from sqlmodel import create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import urllib.parse

# Load environment variables
load_dotenv()

def clean_database_url(original_url):
    """
    Clean the database URL by removing unsupported parameters for asyncpg
    """
    if original_url.startswith("postgresql+asyncpg://"):
        # Parse the URL
        parsed = urllib.parse.urlparse(original_url)
        
        # Reconstruct without problematic query parameters
        cleaned_query = []
        for pair in parsed.query.split('&'):
            if pair and '=' in pair:
                key, value = pair.split('=', 1)
                # Remove parameters that asyncpg doesn't support
                if key not in ['sslmode', 'channel_binding']:
                    cleaned_query.append(pair)
        
        # Reconstruct the URL
        if cleaned_query:
            new_query = '&'.join(cleaned_query)
            new_url = parsed._replace(query=new_query).geturl()
        else:
            new_url = parsed._replace(query='').geturl()
        
        return new_url
    
    return original_url

# Database URL - using Neon Serverless PostgreSQL for production
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./todo_app.db")
CLEANED_DATABASE_URL = clean_database_url(DATABASE_URL)

# Create async engine for PostgreSQL (Neon) or SQLite
if CLEANED_DATABASE_URL.startswith("postgresql"):
    # Use async engine for PostgreSQL
    async_engine = create_async_engine(CLEANED_DATABASE_URL)
elif CLEANED_DATABASE_URL.startswith("sqlite"):
    # Use async engine for SQLite
    async_engine = create_async_engine(CLEANED_DATABASE_URL)
else:
    # Default to SQLite for development
    async_engine = create_async_engine("sqlite+aiosqlite:///./todo_app.db")

# Create async session maker
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an async database session
    """
    async with AsyncSessionLocal() as session:
        yield session


# Import models here to ensure tables are created
async def create_db_and_tables():
    """
    Create database tables
    """
    from sqlmodel import SQLModel
    from models.user import User
    from models.todo import Todo

    async with async_engine.begin() as conn:
        # For SQLite, we need to use sync execution
        if CLEANED_DATABASE_URL.startswith("sqlite"):
            await conn.run_sync(SQLModel.metadata.create_all)
        else:
            await conn.run_sync(SQLModel.metadata.create_all)