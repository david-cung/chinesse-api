from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)
    quiz_type = Column(String)  # multiple-choice, matching, sentence, mixed
    score = Column(Integer)
    total_questions = Column(Integer)
    correct_answers = Column(Integer)
    time_spent_seconds = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    lesson = relationship("Lesson")

class WordStats(Base):
    __tablename__ = "word_stats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    vocabulary_id = Column(Integer, ForeignKey("vocabularies.id"))
    right_count = Column(Integer, default=0)
    wrong_count = Column(Integer, default=0)
    last_seen = Column(DateTime, default=datetime.utcnow)
    percent_correct = Column(Float, default=0.0)
    
    # Relationships
    user = relationship("User")
    vocabulary = relationship("Vocabulary")
