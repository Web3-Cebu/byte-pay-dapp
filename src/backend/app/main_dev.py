from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from .api import merchants, payments
from .config import settings
from . import models
from .database import engine
import os

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=f"{settings.PROJECT_NAME} (Development)",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Development server with static file serving enabled"
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    merchants.router,
    prefix=f"{settings.API_V1_STR}/merchants",
    tags=["merchants"]
)

app.include_router(
    payments.router,
    prefix=f"{settings.API_V1_STR}/payments",
    tags=["payments"]
)

# Mount static files for frontend
frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def read_root():
    return {
        "name": f"{settings.PROJECT_NAME} (Development)",
        "version": settings.VERSION,
        "message": "Welcome to BytePay API - Development Server",
        "frontend": "Static files served from /src/frontend/",
        "static_files": "/static/*"
    }

# Serve frontend HTML at root and other routes (catch-all must be last)
@app.get("/{path:path}")
async def serve_frontend(path: str = ""):
    """Serve frontend for all non-API routes"""
    # API routes should not serve frontend
    if path.startswith("api/") or path.startswith("docs") or path.startswith("openapi.json") or path.startswith("static/"):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not found")
    
    frontend_dir = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
    index_path = os.path.join(frontend_dir, "index.html")
    
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Frontend not found")