# routers/lessons.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from database.database import get_db
from models.lesson import (
    Lesson, Vocabulary, LessonObjective, 
    GrammarPoint, GrammarExample, Exercise
)
from models.character import Character
from models.progress import UserProgress, UserItemProgress
from models.user import User
from schemas.schemas import LessonSummary, LessonDetail
from utils.dependencies import get_current_user_optional

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
async def get_lesson_detail(
    lesson_id: int, 
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Get detailed information about a specific lesson with user progress"""
    lesson = db.query(Lesson).options(
        joinedload(Lesson.characters),
        joinedload(Lesson.vocabularies),
        joinedload(Lesson.objectives),
        joinedload(Lesson.grammar_points).joinedload(GrammarPoint.examples),
        joinedload(Lesson.exercises)
    ).filter(Lesson.id == lesson_id).first()
    
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Get user progress for this lesson
    status = "locked"
    progress_percent = None
    learned_vocab_count = 0
    learned_grammar_count = 0
    learned_listening_count = 0
    learned_speaking_count = 0
    
    if current_user:
        # Get this lesson's progress
        user_progress = db.query(UserProgress).filter(
            UserProgress.user_id == current_user.id,
            UserProgress.lesson_id == lesson_id
        ).first()
        
        if user_progress:
            if user_progress.completed:
                status = "completed"
                progress_percent = 100.0
            else:
                status = "in_progress"
                progress_percent = user_progress.progress_percent or 0.0
        else:
            # Check if previous lesson is completed (to determine if this is unlocked)
            previous_lesson = db.query(Lesson).filter(
                Lesson.hsk_level == lesson.hsk_level,
                Lesson.order < lesson.order,
                Lesson.is_published == True
            ).order_by(Lesson.order.desc()).first()
            
            if previous_lesson:
                prev_progress = db.query(UserProgress).filter(
                    UserProgress.user_id == current_user.id,
                    UserProgress.lesson_id == previous_lesson.id,
                    UserProgress.completed == True
                ).first()
                
                if prev_progress:
                    status = "in_progress"  # Available to start
                    progress_percent = 0.0
                else:
                    status = "locked"
            else:
                # First lesson in level - always available
                status = "in_progress"
                progress_percent = 0.0

        # Calculate learned items
        # 1. Vocabulary
        vocab_ids = [v.id for v in lesson.vocabularies]
        if vocab_ids:
            learned_vocab_count = db.query(UserItemProgress).filter(
                UserItemProgress.user_id == current_user.id,
                UserItemProgress.item_type == "vocabulary",
                UserItemProgress.item_id.in_(vocab_ids),
                UserItemProgress.completed == True
            ).count()
        
        # 2. Grammar Examples
        grammar_example_ids = []
        for gp in lesson.grammar_points:
            grammar_example_ids.extend([ex.id for ex in gp.examples])
        
        if grammar_example_ids:
            learned_grammar_count = db.query(UserItemProgress).filter(
                UserItemProgress.user_id == current_user.id,
                UserItemProgress.item_type == "grammar_example",
                UserItemProgress.item_id.in_(grammar_example_ids),
                UserItemProgress.completed == True
            ).count()
            
        # 3. Listening & Speaking (these are units)
        from models.unit import Unit
        lesson_units = db.query(Unit).filter(Unit.lesson_id == lesson_id).all()
        listening_unit_ids = [u.id for u in lesson_units if u.type == "listening"]
        speaking_unit_ids = [u.id for u in lesson_units if u.type == "speaking"]
        
        if listening_unit_ids:
            learned_listening_count = db.query(UserItemProgress).filter(
                UserItemProgress.user_id == current_user.id,
                UserItemProgress.item_type == "listening",
                UserItemProgress.item_id.in_(listening_unit_ids),
                UserItemProgress.completed == True
            ).count()
            
        if speaking_unit_ids:
            learned_speaking_count = db.query(UserItemProgress).filter(
                UserItemProgress.user_id == current_user.id,
                UserItemProgress.item_type == "speaking",
                UserItemProgress.item_id.in_(speaking_unit_ids),
                UserItemProgress.completed == True
            ).count()
    
    # Format grammar data based on vocabulary examples
    # Each vocabulary word has its corresponding example sentences
    grammar_data = []
    for vocab in lesson.vocabularies:
        grammar_data.append({
            "id": vocab.id,
            "title": vocab.word,
            "explanation": f"{vocab.pinyin} - {vocab.meaning}",
            "examples": [
                {
                    "id": ex.id,
                    "example": ex.sentence,
                    "translation": ex.translation,
                    "order": ex.order
                }
                for ex in sorted(vocab.examples, key=lambda x: x.order)
            ]
        })
    
    return {
        "id": lesson.id,
        "title": lesson.title,
        "description": lesson.description,
        "hsk_level": lesson.hsk_level,
        "estimated_time": lesson.estimated_time,
        "vocabCount": len(lesson.vocabularies),
        "durationMinutes": lesson.estimated_time or 0,
        "status": status,
        "progressPercent": progress_percent,
        "learnedVocabCount": learned_vocab_count,
        "learnedGrammarCount": learned_grammar_count,
        "learnedListeningCount": learned_listening_count,
        "learnedSpeakingCount": learned_speaking_count,
        "characters": lesson.characters,
        "vocabulary": lesson.vocabularies,
        "objectives": sorted(lesson.objectives, key=lambda x: x.order),
        "grammar": grammar_data,
        "exercises": sorted(lesson.exercises, key=lambda x: x.order)
    }


