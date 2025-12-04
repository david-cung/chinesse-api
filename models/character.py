# models/character.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.database import Base
from models.lesson import lesson_characters  # Import the association table

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    character = Column(String(10), nullable=False, unique=True, index=True)
    pinyin = Column(String(50), nullable=False)
    meaning = Column(String(255), nullable=False)
    stroke_count = Column(Integer)
    radical = Column(String(10))
    hsk_level = Column(Integer, index=True)
    audio_url = Column(String(255))
    
    # Relationship - use string reference
    lessons = relationship("Lesson", secondary=lesson_characters, back_populates="characters")
