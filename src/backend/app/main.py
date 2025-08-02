from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import merchants, payments
from .config import settings
from . import models
from .database import engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
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

@app.get("/")
def read_root():
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "message": "Welcome to BytePay API"
    }