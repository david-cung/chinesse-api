from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ==================== User Schemas ====================
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class GoogleAuthRequest(BaseModel):
    """Schema for Google OAuth login/register"""
    id_token: str  # Google ID token from client


class UserResponse(UserBase):
    id: int
    level: int
    xp: int
    streak: int
    gems: int
    avatar: Optional[str] = None
    full_name: Optional[str] = None
    auth_provider: str = "email"
    is_verified: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


class UserSummaryResponse(BaseModel):
    """Summary response for home screen"""
    id: str
    name: str
    greeting: str
    streakDays: int
    avatarUrl: Optional[str] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenWithUser(BaseModel):
    """Token response with user data included"""
    access_token: str
    token_type: str
    user: UserResponse



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
class VocabularyExampleBase(BaseModel):
    sentence: str
    pinyin: Optional[str] = None
    translation: Optional[str] = None


class VocabularyExampleResponse(VocabularyExampleBase):
    id: int
    order: int = 0

    class Config:
        from_attributes = True


class VocabularyBase(BaseModel):
    word: str
    pinyin: str
    meaning: str
    example: Optional[str] = None  # Legacy field


class VocabularyCreate(VocabularyBase):
    hsk_level: int


class VocabularyResponse(VocabularyBase):
    id: int
    hsk_level: Optional[int] = None
    examples: List[VocabularyExampleResponse] = []

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


class LessonWithProgress(BaseModel):
    """Schema cho bài học kèm tiến độ học của user"""
    id: int
    title: str
    description: Optional[str] = None
    hsk_level: int
    order: int = 0
    character_count: int = 0
    vocabulary_count: int = 0
    exercise_count: int = 0
    estimated_time: int = 30
    
    # Trạng thái tiến độ của user
    is_started: bool = False  # User đã bắt đầu học bài này chưa
    is_completed: bool = False  # User đã hoàn thành bài này chưa
    progress_percent: float = 0.0  # Tiến độ học (0-100%)
    score: Optional[int] = None  # Điểm số cao nhất
    exercises_completed: int = 0  # Số bài tập đã làm
    last_accessed_at: Optional[datetime] = None  # Lần cuối học
    
    class Config:
        from_attributes = True


class HSKLevelLessonsResponse(BaseModel):
    """Response cho danh sách bài học theo HSK level"""
    hsk_level: int
    total_lessons: int
    completed_lessons: int
    overall_progress: float  # Tiến độ tổng thể của cấp độ này
    lessons: List[LessonWithProgress]
    
    class Config:
        from_attributes = True


class LessonDetail(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    hsk_level: int
    estimated_time: int = 30
    # New fields for progress tracking
    vocabCount: int = 0
    durationMinutes: int = 0
    status: str = "locked"  # "completed", "in_progress", "locked"
    progressPercent: Optional[float] = None
    # Learned counts
    learnedVocabCount: int = 0
    learnedGrammarCount: int = 0
    learnedListeningCount: int = 0
    learnedSpeakingCount: int = 0
    # Content
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


# ==================== Learning Continue Schemas ====================
class CourseInfo(BaseModel):
    id: str
    level: str


class LessonInfo(BaseModel):
    id: str
    title: str
    description: Optional[str] = None


class ProgressInfo(BaseModel):
    completedPercent: float
    lastUnitId: Optional[str] = None


class LearningContinueResponse(BaseModel):
    course: CourseInfo
    lesson: LessonInfo
    progress: ProgressInfo


# ==================== Course Lessons Schemas ====================
class LessonItem(BaseModel):
    """Individual lesson in course listing"""
    id: str
    title: str
    vocabCount: int
    durationMinutes: int
    status: str  # "completed", "in_progress", "locked"
    progressPercent: Optional[float] = None  # Only for in_progress


class CourseLessonsResponse(BaseModel):
    """Response for GET /courses/{courseId}/lessons"""
    course: CourseInfo
    lessons: List[LessonItem]


# ==================== Learning Resume Schemas ====================
class ResumeUnitInfo(BaseModel):
    """Unit info for resume response"""
    id: str
    type: str
    order: int


class ResumeProgressInfo(BaseModel):
    """Progress info for resume response"""
    lessonPercent: float
    unitPercent: float


class ResumeNavigationInfo(BaseModel):
    """Navigation info for resume response"""
    screen: str
    params: dict


class LearningResumeResponse(BaseModel):
    """Response for GET /api/v1/learning/resume"""
    course: CourseInfo
    lesson: LessonInfo
    unit: ResumeUnitInfo
    progress: ResumeProgressInfo
    navigation: ResumeNavigationInfo


class TrackItemRequest(BaseModel):
    """Yêu cầu đánh dấu một mục nội dung đã được học/truy cập"""
    item_type: str  # "vocabulary", "grammar_example", "listening", "speaking", "character"
    item_id: int
    completed: bool = True
