from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime

class Sentence(Base):
    __tablename__ = "sentences"

    id = Column(Integer, primary_key=True, index=True)
    characters = Column(Text, nullable=False)
    pinyin = Column(Text)
    meaning = Column(Text)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)
    subunit = Column(Integer, nullable=True)
    order = Column(Integer, default=0)
    audio_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    lesson = relationship("Lesson", back_populates="sentences")

# Update Lesson model to have a relationship with sentences
# Note: This will be handled in Lesson model modification if needed, 
# but SQLAlchemy allows defining it here or via back_populates.
