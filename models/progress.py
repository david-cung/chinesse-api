from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, String, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base

class UserProgress(Base):
    __tablename__ = "user_progress"
    __table_args__ = (
        UniqueConstraint('user_id', 'lesson_id', name='unique_user_lesson'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Tiến độ bài học (0-100%)
    progress_percent = Column(Float, default=0.0)
    
    # Đã hoàn thành bài học chưa
    completed = Column(Boolean, default=False)
    
    # Điểm số cao nhất (0-100)
    score = Column(Integer, default=0)
    
    # Số lần exercise đã làm
    exercises_completed = Column(Integer, default=0)
    
    # Timestamps
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    last_accessed_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="progress")
    lesson = relationship("Lesson", backref="user_progress")

class DailyMission(Base):
    __tablename__ = "daily_missions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    target = Column(Integer, nullable=False)
    reward_xp = Column(Integer, default=10)

class UserMission(Base):
    __tablename__ = "user_missions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mission_id = Column(Integer, ForeignKey("daily_missions.id"), nullable=False)
    progress = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    date = Column(DateTime(timezone=True), server_default=func.now())