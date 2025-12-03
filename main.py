from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine, Base
from routers import auth, users, characters, lessons, leaderboard, missions

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tian Tian API",
    version="1.0.0",
    description="Chinese Learning Platform API"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(characters.router)
app.include_router(lessons.router)
app.include_router(leaderboard.router)
app.include_router(missions.router)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)