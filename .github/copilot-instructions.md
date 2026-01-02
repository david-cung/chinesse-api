# Tian Tian Backend - AI Coding Guidelines

## Architecture Overview
FastAPI-based Chinese learning platform with SQLAlchemy ORM. Core components:
- **Models** (`models/`): User progress, characters, lessons with vocab/grammar/exercises
- **Routers** (`routers/`): REST API endpoints (auth, users, characters, lessons, leaderboard, missions)
- **Schemas** (`schemas/schemas.py`): Pydantic models for request/response validation
- **Database** (`database/database.py`): PostgreSQL with SQLAlchemy session management

All models must be imported in `main.py` for SQLAlchemy registration. Uses JWT authentication with PBKDF2 password hashing.

## Key Patterns
- **Auth Flow**: Use `get_current_user` dependency from `utils/dependencies.py` for protected routes
- **DB Access**: Inject `db: Session = Depends(get_db)` in router functions
- **Response Models**: Always use Pydantic schemas from `schemas/schemas.py` for API responses
- **Logging**: Use `logger.info/error` configured in `main.py` (writes to `api.log`)

## Development Workflow
- **Run Locally**: `uvicorn main:app --reload` (requires venv activation)
- **Seed Database**: `python seed/seed_data.py` (drops and recreates tables)
- **API Docs**: Visit `/docs` for interactive Swagger UI
- **Database**: Defaults to SQLite (`tiantian.db`) via `.env` override; production uses PostgreSQL

## Conventions
- Router prefixes: `/auth`, `/users`, `/characters`, `/lessons`, `/leaderboard`, `/missions`
- Model relationships: Use association tables for many-to-many (e.g., `lesson_characters`, `lesson_vocabulary`)
- Error Handling: Raise `HTTPException` with appropriate status codes
- Imports: Absolute imports from project root (e.g., `from models.user import User`)

## Examples
- **Protected Route**: `@router.get("/me", response_model=UserResponse, dependencies=[Depends(get_current_user)])`
- **DB Query**: `user = db.query(User).filter(User.id == user_id).first()`
- **Seed Pattern**: Import all models/associations before `Base.metadata.drop_all/create_all`

Reference: `main.py` for app setup, `routers/users.py` for endpoint patterns, `seed/seed_data.py` for data seeding.