from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database.database import get_db
from models.lesson import Lesson
from models.progress import UserProgress
from models.user import User
from schemas.schemas import LessonResponse
from utils.dependencies import get_current_user
from datetime import datetime

router = APIRouter(prefix="/lessons", tags=["lessons"])

@router.get("/", response_model=List[LessonResponse])
def get_lessons(
    hsk_level: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Lesson)
    if hsk_level:
        query = query.filter(Lesson.hsk_level == hsk_level)
    return query.order_by(Lesson.order).all()

@router.post("/{lesson_id}/complete")
def complete_lesson(
    lesson_id: int,
    score: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.lesson_id == lesson_id
    ).first()
    
    if progress:
        progress.completed = True
        progress.score = max(progress.score, score)
        progress.completed_at = datetime.utcnow()
    else:
        progress = UserProgress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            completed=True,
            score=score,
            completed_at=datetime.utcnow()
        )
        db.add(progress)
    
    xp_earned = score
    current_user.xp += xp_earned
    current_user.level = (current_user.xp // 100) + 1
    
    db.commit()
    
    return {
        "message": "Lesson completed",
        "xp_earned": xp_earned,
        "new_xp": current_user.xp,
        "new_level": current_user.level
    }