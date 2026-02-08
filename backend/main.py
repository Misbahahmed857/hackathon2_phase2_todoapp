from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables
from routers import auth, todos
import os
from fastapi.responses import RedirectResponse
import logging

# Disable the database initialization in lifespan for now to allow server to start
# Database initialization can be handled separately or manually
async def initialize_db():
    try:
        await create_db_and_tables()
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Database initialization failed: {e}")
        # Continue without database if initialization fails


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables
    try:
        await create_db_and_tables()
    except Exception as e:
        print(f"Database initialization error: {e}")
    yield


# Create FastAPI app with lifespan
app = FastAPI(
    title="Todo Web Application API",
    description="API for the Todo Web Application with user authentication and task management",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(todos.router)


@app.get("/")
def read_root():
    """
    Root endpoint to verify API is running
    """
    return {"message": "Todo Web Application API is running!"}


@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "service": "todo-api"}


# Redirect to docs by default
@app.get("/docs", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=True
    )