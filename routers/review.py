from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from database.database import get_db
from models.review import ReviewCard, ReviewRating, ReviewSession
from models.lesson import Vocabulary
from schemas import schemas
from utils.dependencies import get_current_user
from models.user import User

router = APIRouter(
    prefix="/api/v1/review",
    tags=["review"]
)

@router.get("/due", response_model=List[schemas.ReviewCardResponse])
def get_due_cards(
    deck: str = "default",
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get cards due for review (SRS: show_next <= now)"""
    now = datetime.utcnow()
    cards = db.query(ReviewCard).filter(
        ReviewCard.user_id == current_user.id,
        ReviewCard.deck == deck,
        ReviewCard.show_next <= now
    ).order_by(ReviewCard.show_next).limit(limit).all()
    
    return cards

@router.post("/answer", response_model=schemas.ReviewCardResponse)
def submit_review_answer(
    answer: schemas.ReviewAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit review answer and update show_next based on rating"""
    card = db.query(ReviewCard).filter(
        ReviewCard.id == answer.card_id,
        ReviewCard.user_id == current_user.id
    ).first()
    
    if not card:
        raise HTTPException(status_code=404, detail="Review card not found")
    
    rating = db.query(ReviewRating).filter(ReviewRating.id == answer.rating_id).first()
    if not rating:
        raise HTTPException(status_code=400, detail="Invalid rating ID")
    
    # Update card
    card.rating_id = rating.id
    card.show_next = datetime.utcnow() + timedelta(minutes=rating.duration_minutes)
    
    db.commit()
    db.refresh(card)
    
    return card

@router.post("/add", status_code=status.HTTP_201_CREATED)
def add_to_review(
    vocabulary_id: int,
    deck: str = "default",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a word to the review deck manually (or automatically after learning)"""
    # Check if already in review
    existing = db.query(ReviewCard).filter(
        ReviewCard.user_id == current_user.id,
        ReviewCard.vocabulary_id == vocabulary_id
    ).first()
    
    if existing:
        return {"message": "Word already in review deck"}
    
    new_card = ReviewCard(
        user_id=current_user.id,
        vocabulary_id=vocabulary_id,
        deck=deck,
        show_next=datetime.utcnow()  # Due immediately
    )
    
    db.add(new_card)
    db.commit()
    
    return {"message": "Added to review deck"}

@router.get("/status", response_model=schemas.ReviewStatusResponse)
def get_review_status(
    deck: str = "default",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get number of cards due for review"""
    now = datetime.utcnow()
    due_count = db.query(ReviewCard).filter(
        ReviewCard.user_id == current_user.id,
        ReviewCard.deck == deck,
        ReviewCard.show_next <= now
    ).count()
    
    return {"due_count": due_count, "deck_name": deck}

@router.get("/ratings", response_model=List[schemas.ReviewRatingResponse])
def get_review_ratings(db: Session = Depends(get_db)):
    """Get all available review ratings and their durations"""
    ratings = db.query(ReviewRating).all()
    if not ratings:
        # Default ratings if table is empty
        return [
            {"id": 1, "name": "Again", "duration_minutes": 1},
            {"id": 2, "name": "Hard", "duration_minutes": 1440},  # 1 day
            {"id": 3, "name": "Good", "duration_minutes": 4320},  # 3 days
            {"id": 4, "name": "Easy", "duration_minutes": 10080}, # 7 days
        ]
    return ratings
