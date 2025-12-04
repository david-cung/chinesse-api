from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from models.progress import DailyMission, UserMission
from models.user import User
from schemas.schemas import DailyMissionResponse
from utils.dependencies import get_current_user
from datetime import datetime, date

router = APIRouter(prefix="/missions", tags=["missions"])

@router.get("/daily", response_model=List[DailyMissionResponse])
def get_daily_missions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    missions = db.query(DailyMission).all()
    
    today = date.today()
    user_missions = db.query(UserMission).filter(
        UserMission.user_id == current_user.id,
        UserMission.date >= datetime(today.year, today.month, today.day)
    ).all()
    
    response = []
    for mission in missions:
        user_mission = next(
            (um for um in user_missions if um.mission_id == mission.id),
            None
        )
        
        response.append(DailyMissionResponse(
            id=mission.id,
            title=mission.title,
            description=mission.description,
            progress=user_mission.progress if user_mission else 0,
            target=mission.target,
            completed=user_mission.completed if user_mission else False,
            reward_xp=mission.reward_xp
        ))
    
    return response

@router.post("/{mission_id}/complete")
def complete_mission(
    mission_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mission = db.query(DailyMission).filter(DailyMission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    user_mission = db.query(UserMission).filter(
        UserMission.user_id == current_user.id,
        UserMission.mission_id == mission_id
    ).first()
    
    if user_mission:
        user_mission.completed = True
        user_mission.progress = mission.target
    
    current_user.xp += mission.reward_xp
    current_user.level = (current_user.xp // 100) + 1
    
    db.commit()
    
    return {"message": "Mission completed", "xp_earned": mission.reward_xp}

@router.get("/{mission_id}", response_model=DailyMissionResponse)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    """
    Get a specific mission by ID
    """
    mission = db.query(DailyMission).filter(DailyMission.id == mission_id).first()
    
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    return mission