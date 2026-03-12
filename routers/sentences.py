from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from models.sentence import Sentence
from schemas import schemas
from utils.dependencies import get_current_user
from models.user import User

router = APIRouter(
    prefix="/api/v1/sentences",
    tags=["sentences"]
)

@router.get("/lesson/{lesson_id}", response_model=List[schemas.SentenceResponse])
def get_lesson_sentences(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all sentences associated with a lesson"""
    sentences = db.query(Sentence).filter(Sentence.lesson_id == lesson_id).all()
    return sentences

@router.get("/word/{word}", response_model=List[schemas.SentenceResponse])
def get_word_sentences(
    word: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get sentences containing a specific word"""
    sentences = db.query(Sentence).filter(Sentence.characters.like(f"%{word}%")).limit(10).all()
    return sentences
