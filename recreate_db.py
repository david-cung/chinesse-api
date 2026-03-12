# recreate_db.py
from database.database import engine, Base
# Import all models to ensure they are registered with Base.metadata
from models import user, character, progress, unit, review, quiz, sentence
from models.lesson import (
    Lesson, Vocabulary, LessonObjective,
    GrammarPoint, GrammarExample, Exercise,
    lesson_characters, lesson_vocabulary
)

def recreate_db():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Done!")

if __name__ == "__main__":
    recreate_db()
