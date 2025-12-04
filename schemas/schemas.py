from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ==================== User Schemas ====================
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


# ==================== Character Schemas ====================
class CharacterBase(BaseModel):
    character: str
    pinyin: str
    meaning: str
    stroke_count: Optional[int] = None
    radical: Optional[str] = None


class CharacterCreate(CharacterBase):
    hsk_level: int
    audio_url: Optional[str] = None


class CharacterResponse(CharacterBase):
    id: int

    class Config:
        from_attributes = True


# ==================== Vocabulary Schemas ====================
class VocabularyBase(BaseModel):
    word: str
    pinyin: str
    meaning: str
    example: Optional[str] = None


class VocabularyCreate(VocabularyBase):
    hsk_level: int


class VocabularyResponse(VocabularyBase):
    id: int
    hsk_level: Optional[int] = None

    class Config:
        from_attributes = True


# ==================== Grammar Schemas ====================
class GrammarExampleBase(BaseModel):
    example: str
    translation: Optional[str] = None


class GrammarExampleResponse(GrammarExampleBase):
    id: int
    order: int

    class Config:
        from_attributes = True


class GrammarPointBase(BaseModel):
    title: str
    explanation: str


class GrammarPointCreate(GrammarPointBase):
    examples: List[GrammarExampleBase] = []


class GrammarPointResponse(GrammarPointBase):
    id: int
    examples: List[GrammarExampleResponse] = []

    class Config:
        from_attributes = True


# ==================== Exercise Schemas ====================
class ExerciseBase(BaseModel):
    type: str  # multiple_choice, fill_blank, matching, etc.
    question: str
    answer: str
    options: Optional[str] = None  # JSON string


class ExerciseCreate(ExerciseBase):
    order: int = 0


class ExerciseResponse(ExerciseBase):
    id: int
    order: int

    class Config:
        from_attributes = True


# ==================== Lesson Objective Schema ====================
class LessonObjectiveBase(BaseModel):
    objective: str


class LessonObjectiveResponse(LessonObjectiveBase):
    id: int
    order: int

    class Config:
        from_attributes = True


# ==================== Lesson Schemas ====================
class LessonBase(BaseModel):
    title: str
    description: Optional[str] = None
    hsk_level: int


class LessonCreate(LessonBase):
    estimated_time: int = 30
    order: int = 0
    is_published: bool = True


class LessonSummary(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    hsk_level: int
    character_count: int
    vocabulary_count: int = 0
    estimated_time: int = 30
    completed: bool = False

    class Config:
        from_attributes = True


class LessonDetail(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    hsk_level: int
    estimated_time: int = 30
    characters: List[CharacterResponse] = []
    vocabulary: List[VocabularyResponse] = []
    objectives: List[LessonObjectiveResponse] = []
    grammar: List[GrammarPointResponse] = []
    exercises: List[ExerciseResponse] = []

    class Config:
        from_attributes = True


class LessonResponse(LessonBase):
    id: int
    characters: List[CharacterResponse] = []
    estimated_time: int = 30

    class Config:
        from_attributes = True


# ==================== Progress Schemas ====================
class UserLessonProgressBase(BaseModel):
    lesson_id: int
    completed: bool = False
    score: Optional[int] = None


class UserLessonProgressCreate(UserLessonProgressBase):
    user_id: int


class UserLessonProgressResponse(UserLessonProgressBase):
    id: int
    user_id: int
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== Mission Schemas ====================
class DailyMissionBase(BaseModel):
    title: str
    description: str
    target: int
    reward_xp: int


class DailyMissionResponse(DailyMissionBase):
    id: int
    progress: int
    completed: bool

    class Config:
        from_attributes = True


# ==================== Leaderboard Schema ====================
class LeaderboardEntry(BaseModel):
    rank: int
    user_id: int
    username: str
    xp: int
    level: int = 1
    avatar: Optional[str] = None

    class Config:
        from_attributes = True


# ==================== Practice Schemas ====================
class PracticeSessionBase(BaseModel):
    lesson_id: int
    score: int
    total_questions: int
    correct_answers: int


class PracticeSessionCreate(PracticeSessionBase):
    user_id: int
    time_spent: int  # seconds


class PracticeSessionResponse(PracticeSessionBase):
    id: int
    user_id: int
    time_spent: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Statistics Schemas ====================
class UserStatsResponse(BaseModel):
    total_lessons_completed: int
    total_characters_learned: int
    total_vocabulary_learned: int
    total_practice_time: int  # minutes
    current_streak: int
    longest_streak: int
    total_xp: int
    level: int

    class Config:
        from_attributes = True
