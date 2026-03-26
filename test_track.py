import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database import Base
from models.lesson import Lesson, Vocabulary
from models.user import User
from models.progress import UserItemProgress, UserProgress

# We won't run the whole FastAPI app, just test the DB query logic
engine = create_engine('postgresql://postgres:postgres@localhost:5432/chinesse_db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

user_id = 1
item_id = 1
completed = True

try:
    lesson_id = None
    vocab = db.query(Vocabulary).filter(Vocabulary.id == item_id).first()
    if vocab:
        lesson_id = vocab.lesson_id

    if lesson_id:
        lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if lesson:
            vocab_list = lesson.vocabularies
            total_items = len(vocab_list) if vocab_list else 0
            
            if total_items > 0:
                vocab_ids = [v.id for v in vocab_list]
                
                completed_items_count = db.query(UserItemProgress).filter(
                    UserItemProgress.user_id == user_id,
                    UserItemProgress.item_type == "vocabulary",
                    UserItemProgress.item_id.in_(vocab_ids),
                    UserItemProgress.completed == True
                ).count()
                
                print(f"Total: {total_items}, Completed: {completed_items_count}")
                new_progress = min(100.0, (completed_items_count / total_items) * 100)
                print(f"New Progress: {new_progress}")
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
