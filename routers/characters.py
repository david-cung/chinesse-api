from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from typing import List, Optional
from database.database import get_db
from models.character import Character
from schemas.schemas import CharacterResponse

router = APIRouter(prefix="/characters", tags=["characters"])

@router.get("/", response_model=List[CharacterResponse])
def get_characters(
    hsk_level: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Character)
    if hsk_level:
        query = query.filter(Character.hsk_level == hsk_level)
    return query.all()

@router.get("/random", response_model=List[CharacterResponse])
def get_random_characters(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Fetch random characters for quick access on Home screen"""
    return db.query(Character).order_by(func.random()).limit(limit).all()

@router.get("/{character_id}", response_model=CharacterResponse)
def get_character(character_id: int, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character