from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from database.database import Base

lesson_characters = Table(
    'lesson_characters',
    Base.metadata,
    Column('lesson_id', Integer, ForeignKey('lessons.id')),
    Column('character_id', Integer, ForeignKey('characters.id'))
)

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    hsk_level = Column(Integer, nullable=False, index=True)
    order = Column(Integer, default=0)
    
    characters = relationship("Character", secondary=lesson_characters)