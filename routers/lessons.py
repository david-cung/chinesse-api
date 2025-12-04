# routers/lessons.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from typing import List
from database.database import get_db
from models.lesson import (
    Lesson, Vocabulary, LessonObjective, 
    GrammarPoint, GrammarExample, Exercise
)
from models.character import Character
from schemas.schemas import LessonSummary, LessonDetail

router = APIRouter(prefix="/api/lessons", tags=["lessons"])

@router.get("", response_model=List[LessonSummary])
async def get_lessons(hsk_level: int = 1, db: Session = Depends(get_db)):
    """Get all lessons for a specific HSK level"""
    lessons = db.query(Lesson).filter(
        Lesson.hsk_level == hsk_level,
        Lesson.is_published == True
    ).order_by(Lesson.order).all()
    
    result = []
    for lesson in lessons:
        result.append(LessonSummary(
            id=lesson.id,
            title=lesson.title,
            description=lesson.description,
            hsk_level=lesson.hsk_level,
            character_count=len(lesson.characters),
            vocabulary_count=len(lesson.vocabularies),
            estimated_time=lesson.estimated_time,
            completed=False
        ))
    
    return result

@router.get("/{lesson_id}", response_model=LessonDetail)
async def get_lesson_detail(lesson_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific lesson"""
    lesson = db.query(Lesson).options(
        joinedload(Lesson.characters),
        joinedload(Lesson.vocabularies),
        joinedload(Lesson.objectives),
        joinedload(Lesson.grammar_points).joinedload(GrammarPoint.examples),
        joinedload(Lesson.exercises)
    ).filter(Lesson.id == lesson_id).first()
    
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Format grammar points with examples
    grammar_data = []
    for gp in sorted(lesson.grammar_points, key=lambda x: x.order):
        grammar_data.append({
            "id": gp.id,
            "title": gp.title,
            "explanation": gp.explanation,
            "examples": [
                {
                    "id": ex.id,
                    "example": ex.example,
                    "translation": ex.translation,
                    "order": ex.order
                }
                for ex in sorted(gp.examples, key=lambda x: x.order)
            ]
        })
    
    return {
        "id": lesson.id,
        "title": lesson.title,
        "description": lesson.description,
        "hsk_level": lesson.hsk_level,
        "estimated_time": lesson.estimated_time,
        "characters": lesson.characters,
        "vocabulary": lesson.vocabularies,
        "objectives": sorted(lesson.objectives, key=lambda x: x.order),
        "grammar": grammar_data,
        "exercises": sorted(lesson.exercises, key=lambda x: x.order)
    }
