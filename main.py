# main.py
import sys
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine, Base

# Configure logging (no emojis for Windows)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Import ALL models to register with SQLAlchemy
logger.info("Importing models...")
from models import user, character, progress, unit
from models.lesson import (
    Lesson, Vocabulary, LessonObjective,
    GrammarPoint, GrammarExample, Exercise,
    lesson_characters, lesson_vocabulary
)

# Create tables
logger.info("Creating database tables...")
try:
    Base.metadata.create_all(bind=engine)
    logger.info("[SUCCESS] Database tables created!")
except Exception as e:
    logger.error(f"[ERROR] Error creating tables: {e}")

# Create FastAPI app
app = FastAPI(
    title="Tian Tian API",
    version="1.0.0",
    description="Chinese Learning Platform API"
)

# CORS - Allow React Native and web apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for mobile apps
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from routers import auth, users, characters, lessons, leaderboard, missions, learning, pronunciation

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(characters.router)
app.include_router(lessons.router)
app.include_router(leaderboard.router)
app.include_router(missions.router)
app.include_router(learning.router)
app.include_router(pronunciation.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Tian Tian API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    logger.info("=" * 80)
    logger.info("[STARTUP] Tian Tian API Server Starting...")
    logger.info("=" * 80)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("[SHUTDOWN] Server shutting down...")
