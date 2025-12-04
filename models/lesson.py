# models/lesson.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from database.database import Base

# Association Tables
lesson_characters = Table(
    'lesson_characters',
    Base.metadata,
    Column('lesson_id', Integer, ForeignKey('lessons.id', ondelete='CASCADE')),
    Column('character_id', Integer, ForeignKey('characters.id', ondelete='CASCADE'))
)

lesson_vocabulary = Table(
    'lesson_vocabulary',
    Base.metadata,
    Column('lesson_id', Integer, ForeignKey('lessons.id', ondelete='CASCADE')),
    Column('vocabulary_id', Integer, ForeignKey('vocabularies.id', ondelete='CASCADE'))
)

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    hsk_level = Column(Integer, nullable=False, index=True)
    order = Column(Integer, default=0)
    estimated_time = Column(Integer, default=30)
    is_published = Column(Boolean, default=True)
    
    # Relationships - use string references to avoid circular imports
    characters = relationship("Character", secondary=lesson_characters, back_populates="lessons")
    vocabularies = relationship("Vocabulary", secondary=lesson_vocabulary, back_populates="lessons")
    objectives = relationship("LessonObjective", back_populates="lesson", cascade="all, delete-orphan")
    grammar_points = relationship("GrammarPoint", back_populates="lesson", cascade="all, delete-orphan")
    exercises = relationship("Exercise", back_populates="lesson", cascade="all, delete-orphan")


class Vocabulary(Base):
    __tablename__ = "vocabularies"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(50), nullable=False, index=True)
    pinyin = Column(String(100), nullable=False)
    meaning = Column(String(255), nullable=False)
    example = Column(Text)
    hsk_level = Column(Integer, index=True)
    
    lessons = relationship("Lesson", secondary=lesson_vocabulary, back_populates="vocabularies")


class LessonObjective(Base):
    __tablename__ = "lesson_objectives"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False)
    objective = Column(Text, nullable=False)
    order = Column(Integer, default=0)
    
    lesson = relationship("Lesson", back_populates="objectives")


class GrammarPoint(Base):
    __tablename__ = "grammar_points"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(255), nullable=False)
    explanation = Column(Text, nullable=False)
    order = Column(Integer, default=0)
    
    lesson = relationship("Lesson", back_populates="grammar_points")
    examples = relationship("GrammarExample", back_populates="grammar_point", cascade="all, delete-orphan")


class GrammarExample(Base):
    __tablename__ = "grammar_examples"

    id = Column(Integer, primary_key=True, index=True)
    grammar_point_id = Column(Integer, ForeignKey('grammar_points.id', ondelete='CASCADE'), nullable=False)
    example = Column(Text, nullable=False)
    translation = Column(Text)
    order = Column(Integer, default=0)
    
    grammar_point = relationship("GrammarPoint", back_populates="examples")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False)
    type = Column(String(50), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(String(255), nullable=False)
    options = Column(Text)
    order = Column(Integer, default=0)
    
    lesson = relationship("Lesson", back_populates="exercises")
