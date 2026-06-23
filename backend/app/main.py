"""
FastAPI main application.
AI Academic Content Detector - Backend Server.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.ml.train import is_trained, train_models
from app.ml.predict import load_model
from app.routes import analysis, model_info, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic."""
    # Initialize database
    try:
        print("Initializing database...")
        init_db()
    except Exception as e:
        print(f"CRITICAL: Database initialization failed: {e}")

    # Auto-train model if not already trained
    try:
        if not is_trained():
            print("No trained model found. Training initial model...")
            train_models()
    except Exception as e:
        print(f"CRITICAL: Auto-training failed: {e}")

    # Load model into memory
    try:
        print("Loading model...")
        load_model()
    except Exception as e:
        print(f"CRITICAL: Model loading failed: {e}")

    print("OK - Server ready!")
    yield
    print("Server shutting down.")


# Create FastAPI app
app = FastAPI(
    title="AI Academic Content Detector",
    description="Detect whether academic text is AI-generated or Human-written using Machine Learning.",
    version="1.0.0",
    lifespan=lifespan,
)

from fastapi import Request
from fastapi.responses import JSONResponse
import traceback

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    tb = traceback.format_exc()
    print(f"Unhandled exception occurred: {exc}\n{tb}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": f"Internal Server Error: {str(exc)}",
            "traceback": tb
        }
    )

# CORS - allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(analysis.router)
app.include_router(model_info.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    return {"message": "AI Academic Content Detector API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy", "model_trained": is_trained()}
