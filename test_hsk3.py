import sys
import os
sys.path.append(os.getcwd())
from database.database import SessionLocal
from models.user import User
from models.lesson import Lesson
from models.progress import UserProgress

db = SessionLocal()
user = db.query(User).first()
if not user:
    print("No user found")
    sys.exit(0)

print(f"User: {user.username}")

# Find an HSK 3 lesson
lesson3 = db.query(Lesson).filter(Lesson.hsk_level == 3).first()
if not lesson3:
    print("No HSK 3 lesson found")
else:
    print(f"HSK 3 Lesson found: {lesson3.id} - {lesson3.title}")
    
# Check resume endpoint logic
from routers.learning import get_learning_resume
try:
    resume = get_learning_resume(current_user=user, db=db)
    print("Resume logic succeeded:", resume.model_dump_json())
except Exception as e:
    import traceback
    print("Error in resume logic:")
    traceback.print_exc()

