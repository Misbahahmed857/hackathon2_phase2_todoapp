from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables
from mcp import Server
from backend.tools.task_operations import server as mcp_server
import os
from fastapi.responses import RedirectResponse
import logging
import threading
import time


# Initialize the MCP server
mcp_server_instance = mcp_server


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables
    try:
        await create_db_and_tables()
    except Exception as e:
        print(f"Database initialization error: {e}")
    
    # Start the MCP server in a separate thread
    def run_mcp_server():
        # Give a small delay to ensure FastAPI server starts first
        time.sleep(1)
        mcp_server_instance.run()
    
    # Run the MCP server in a background thread
    mcp_thread = threading.Thread(target=run_mcp_server, daemon=True)
    mcp_thread.start()
    
    yield
    
    # Shutdown operations can go here if needed


# Create FastAPI app with lifespan
app = FastAPI(
    title="MCP Task Management Server",
    description="Server exposing task management operations as MCP tools",
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


@app.get("/")
def read_root():
    """
    Root endpoint to verify API is running
    """
    return {"message": "MCP Task Management Server is running!", "status": "ready"}


@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "service": "mcp-task-management-server"}


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