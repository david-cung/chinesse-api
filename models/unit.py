# models/unit.py
"""
Unit and UnitProgress models for lesson unit-level tracking.
Unit types: vocabulary, listening, speaking, writing, grammar, exercise
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base


# Unit types mapping to navigation screens
UNIT_TYPE_SCREENS = {
    "vocabulary": "VocabularyPractice",
    "listening": "ListeningPractice",
    "speaking": "SpeakingPractice",
    "writing": "WritingPractice",
    "grammar": "GrammarLesson",
    "exercise": "ExercisePractice",
}


class Unit(Base):
    """
    Represents a learning unit within a lesson.
    Each lesson has multiple units that must be completed in order.
    """
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Unit type: vocabulary, listening, speaking, writing, grammar, exercise
    type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    order = Column(Integer, default=0)  # Order within the lesson
    
    # Optional: reference to content (e.g., vocabulary_id, exercise_id)
    content_type = Column(String(50), nullable=True)  # "vocabulary", "exercise", etc.
    content_id = Column(Integer, nullable=True)
    
    # Estimated duration in minutes
    duration_minutes = Column(Integer, default=5)
    
    # Relationships
    lesson = relationship("Lesson", backref="units")
    
    @property
    def screen_name(self) -> str:
        """Get the navigation screen name for this unit type"""
        return UNIT_TYPE_SCREENS.get(self.type, "LessonDetail")


class UnitProgress(Base):
    """
    Tracks user progress for each unit.
    """
    __tablename__ = "unit_progress"
    __table_args__ = (
        UniqueConstraint('user_id', 'unit_id', name='unique_user_unit'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    unit_id = Column(Integer, ForeignKey("units.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Progress tracking
    progress_percent = Column(Float, default=0.0)  # 0-100%
    completed = Column(Boolean, default=False)
    score = Column(Integer, default=0)  # 0-100
    
    # Timestamps
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    last_accessed_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="unit_progress")
    unit = relationship("Unit", backref="user_progress")
