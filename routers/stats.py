from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta

from database.database import get_db
from models.quiz import QuizAttempt, WordStats
from models.review import ReviewCard
from models.progress import UserProgress
from schemas import schemas
from utils.dependencies import get_current_user
from models.user import User

router = APIRouter(
    prefix="/api/v1/stats",
    tags=["stats"]
)

@router.get("/overview", response_model=schemas.StatsOverviewResponse)
def get_stats_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get weekly overview stats"""
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # New words today (based on UserItemProgress or similar)
    # For now, mock or use basic count
    new_words_today = 0 # Need to implement in progress tracking
    
    # Reviewed today
    reviewed_today = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id,
        QuizAttempt.created_at >= today
    ).count()
    
    # Accuracy
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id,
        QuizAttempt.created_at >= today - timedelta(days=7)
    ).all()
    
    total_q = sum(a.total_questions for a in attempts) if attempts else 0
    total_c = sum(a.correct_answers for a in attempts) if attempts else 0
    accuracy = (total_c / total_q * 100) if total_q > 0 else 0
    
    return {
        "new_words_today": new_words_today,
        "reviewed_today": reviewed_today,
        "accuracy_percent": accuracy,
        "current_streak": current_user.streak
    }

@router.get("/timeline", response_model=schemas.StatsTimelineResponse)
def get_stats_timeline(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get daily right/wrong counts for the timeline chart"""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Group by date
    results = db.query(
        func.date(QuizAttempt.created_at).label("day"),
        func.sum(QuizAttempt.correct_answers).label("right"),
        func.sum(QuizAttempt.total_questions - QuizAttempt.correct_answers).label("wrong")
    ).filter(
        QuizAttempt.user_id == current_user.id,
        QuizAttempt.created_at >= start_date
    ).group_by(func.date(QuizAttempt.created_at)).all()
    
    timeline = []
    # Fill in gaps with 0
    date_map = {str(r.day): r for r in results}
    for i in range(days):
        d = (start_date + timedelta(days=i)).date()
        d_str = str(d)
        if d_str in date_map:
            r = date_map[d_str]
            timeline.append({
                "date": d_str,
                "right_count": int(r.right),
                "wrong_count": int(r.wrong)
            })
        else:
            timeline.append({
                "date": d_str,
                "right_count": 0,
                "wrong_count": 0
            })
            
    return {"timeline": timeline}
