from sqlalchemy import Column, Integer, String, JSON
from database.database import Base

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    character = Column(String, unique=True, nullable=False)
    pinyin = Column(String, nullable=False)
    meaning = Column(String, nullable=False)
    hsk_level = Column(Integer, nullable=False, index=True)
    stroke_order = Column(JSON, nullable=True)
    audio_url = Column(String, nullable=True)