from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from database.database import get_db
from models.user import User
from schemas.schemas import UserResponse, UserSummaryResponse
from utils.dependencies import get_current_user

router = APIRouter(prefix="/api/v1", tags=["users"])


def get_greeting() -> str:
    """Get greeting based on current time of day"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Chào buổi sáng"
    elif 12 <= hour < 18:
        return "Chào buổi chiều"
    else:
        return "Chào buổi tối"

@router.get("/me/summary", response_model=UserSummaryResponse)
def get_user_summary(current_user: User = Depends(get_current_user)):
    """
    Get user summary for home screen.
    
    Returns:
    - id: User ID with prefix "u_"
    - name: User's display name (full_name or username)
    - greeting: Time-based greeting (sáng/chiều/tối)
    - streakDays: Current streak count
    - avatarUrl: User's avatar URL
    """
    return UserSummaryResponse(
        id=f"u_{current_user.id}",
        name=current_user.full_name or current_user.username,
        greeting=get_greeting(),
        streakDays=current_user.streak,
        avatarUrl=current_user.avatar
    )


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
def update_user(
    username: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if username:
        current_user.username = username
    db.commit()
    db.refresh(current_user)
    return current_user