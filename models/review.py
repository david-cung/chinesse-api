from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime

class ReviewRating(Base):
    __tablename__ = "review_ratings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # Again, Hard, Good, Easy
    duration_minutes = Column(Integer)  # Next review after X minutes
    
    # Relationships
    cards = relationship("ReviewCard", back_populates="last_rating")

class ReviewCard(Base):
    __tablename__ = "review_cards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    vocabulary_id = Column(Integer, ForeignKey("vocabularies.id"))
    deck = Column(String, default="default")
    show_next = Column(DateTime, default=datetime.utcnow)
    rating_id = Column(Integer, ForeignKey("review_ratings.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    vocabulary = relationship("Vocabulary")
    last_rating = relationship("ReviewRating", back_populates="cards")

class ReviewSession(Base):
    __tablename__ = "review_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    cards_reviewed = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User")
