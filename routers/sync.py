from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from database.database import get_db
from models.lesson import Lesson, Vocabulary, GrammarPoint, character_lesson, lesson_vocabulary
from models.character import Character
from schemas.schemas import LessonSummary
from typing import List, Dict, Any

router = APIRouter(prefix="/api/v1/sync", tags=["sync"])

@router.get("/full")
async def get_full_sync_data(db: Session = Depends(get_db)):
    """
    Returns all data needed for offline use in the mobile app.
    This includes lessons, vocabularies, grammar points, and their relationships.
    """
    # 1. Fetch all lessons
    lessons = db.query(Lesson).filter(Lesson.is_published == True).all()
    
    # 2. Fetch all vocabularies with their examples
    vocabularies = db.query(Vocabulary).options(
        joinedload(Vocabulary.examples)
    ).all()
    
    # 3. Fetch all grammar points with their examples
    grammar_points = db.query(GrammarPoint).options(
        joinedload(GrammarPoint.examples)
    ).all()
    
    # 4. Fetch all characters
    characters = db.query(Character).all()
    
    # 5. Fetch association tables
    # lesson_vocabulary
    lv_records = db.execute("SELECT lesson_id, vocabulary_id FROM lesson_vocabulary").all()
    lesson_vocab_map = [{"lesson_id": r.lesson_id, "vocabulary_id": r.vocabulary_id} for r in lv_records]
    
    # lesson_characters
    lc_records = db.execute("SELECT lesson_id, character_id FROM lesson_characters").all()
    lesson_char_map = [{"lesson_id": r.lesson_id, "character_id": r.character_id} for r in lc_records]

    return {
        "lessons": lessons,
        "vocabularies": vocabularies,
        "grammar_points": grammar_points,
        "characters": characters,
        "associations": {
            "lesson_vocabulary": lesson_vocab_map,
            "lesson_characters": lesson_char_map
        }
    }
