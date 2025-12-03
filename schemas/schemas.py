from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    level: int
    xp: int
    streak: int
    gems: int
    avatar: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class CharacterBase(BaseModel):
    character: str
    pinyin: str
    meaning: str
    hsk_level: int
    audio_url: Optional[str] = None

class CharacterResponse(CharacterBase):
    id: int

    class Config:
        from_attributes = True

class LessonBase(BaseModel):
    title: str
    description: str
    hsk_level: int

class LessonResponse(LessonBase):
    id: int
    characters: List[CharacterResponse] = []

    class Config:
        from_attributes = True

class DailyMissionResponse(BaseModel):
    id: int
    title: str
    description: str
    progress: int
    target: int
    completed: bool
    reward_xp: int

class LeaderboardEntry(BaseModel):
    rank: int
    user_id: int
    username: str
    xp: int
    avatar: Optional[str] = None