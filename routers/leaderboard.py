from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from models.user import User
from schemas.schemas import LeaderboardEntry

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

@router.get("/", response_model=List[LeaderboardEntry])
def get_leaderboard(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.xp.desc()).limit(10).all()
    
    leaderboard = []
    for rank, user in enumerate(users, 1):
        leaderboard.append(LeaderboardEntry(
            rank=rank,
            user_id=user.id,
            username=user.username,
            xp=user.xp,
            avatar=user.avatar
        ))
    
    return leaderboard