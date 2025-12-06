# seed_hsk234_lessons.py
import sys
sys.path.append('.')

from sqlalchemy.orm import Session
from database.database import SessionLocal, engine
from models.lesson import Lesson

def seed_hsk234_lessons():
    """Seed lesson list for HSK 2, 3, 4"""
    db = SessionLocal()

    try:
        print("=" * 80)
        print("Seeding HSK 2, 3, 4 Lessons List...")
        print("=" * 80)

        # HSK 2 Lessons
        print("\n[1/3] Creating HSK 2 lessons...")
        hsk2_lessons = [
            {
                "title": "Time and Date",
                "description": "Learn to tell time, days, months, and dates",
                "hsk_level": 2,
                "order": 1,
                "estimated_time": 35,
                "is_published": True
            },
            {
                "title": "Weather and Seasons",
                "description": "Describe weather conditions and talk about seasons",
                "hsk_level": 2,
                "order": 2,
                "estimated_time": 30,
                "is_published": True
            },
            {
                "title": "Shopping and Money",
                "description": "Vocabulary for shopping, prices, and transactions",
                "hsk_level": 2,
                "order": 3,
                "estimated_time": 40,
                "is_published": True
            },
            {
                "title": "Daily Activities",
                "description": "Express daily routines and common activities",
                "hsk_level": 2,
                "order": 4,
                "estimated_time": 35,
                "is_published": True
            },
            {
                "title": "Directions and Locations",
                "description": "Ask for and give directions, describe locations",
                "hsk_level": 2,
                "order": 5,
                "estimated_time": 40,
                "is_published": True
            },
            {
                "title": "Food and Dining",
                "description": "Order food, restaurant vocabulary, and preferences",
                "hsk_level": 2,
                "order": 6,
                "estimated_time": 35,
                "is_published": True
            },
        ]

        for lesson_data in hsk2_lessons:
            # Check if lesson already exists
            existing = db.query(Lesson).filter(
                Lesson.title == lesson_data["title"],
                Lesson.hsk_level == lesson_data["hsk_level"]
            ).first()
            
            if not existing:
                lesson = Lesson(**lesson_data)
                db.add(lesson)
            else:
                print(f"   [SKIP] Lesson '{lesson_data['title']}' already exists")
        
        db.commit()
        print(f"   [SUCCESS] Created {len(hsk2_lessons)} HSK 2 lessons")

        # HSK 3 Lessons
        print("\n[2/3] Creating HSK 3 lessons...")
        hsk3_lessons = [
            {
                "title": "Hobbies and Interests",
                "description": "Talk about hobbies, sports, and leisure activities",
                "hsk_level": 3,
                "order": 1,
                "estimated_time": 40,
                "is_published": True
            },
            {
                "title": "Travel and Transportation",
                "description": "Vocabulary for traveling, booking tickets, and transport",
                "hsk_level": 3,
                "order": 2,
                "estimated_time": 45,
                "is_published": True
            },
            {
                "title": "Health and Medical",
                "description": "Describe symptoms, body parts, and medical situations",
                "hsk_level": 3,
                "order": 3,
                "estimated_time": 40,
                "is_published": True
            },
            {
                "title": "Making Plans",
                "description": "Make appointments, discuss schedules and arrangements",
                "hsk_level": 3,
                "order": 4,
                "estimated_time": 35,
                "is_published": True
            },
            {
                "title": "Describing People",
                "description": "Describe personality, appearance, and characteristics",
                "hsk_level": 3,
                "order": 5,
                "estimated_time": 40,
                "is_published": True
            },
            {
                "title": "Life Events",
                "description": "Talk about important life events and experiences",
                "hsk_level": 3,
                "order": 6,
                "estimated_time": 45,
                "is_published": True
            },
        ]

        for lesson_data in hsk3_lessons:
            existing = db.query(Lesson).filter(
                Lesson.title == lesson_data["title"],
                Lesson.hsk_level == lesson_data["hsk_level"]
            ).first()
            
            if not existing:
                lesson = Lesson(**lesson_data)
                db.add(lesson)
            else:
                print(f"   [SKIP] Lesson '{lesson_data['title']}' already exists")
        
        db.commit()
        print(f"   [SUCCESS] Created {len(hsk3_lessons)} HSK 3 lessons")

        # HSK 4 Lessons
        print("\n[3/3] Creating HSK 4 lessons...")
        hsk4_lessons = [
            {
                "title": "Work and Career",
                "description": "Professional vocabulary, job interviews, and workplace",
                "hsk_level": 4,
                "order": 1,
                "estimated_time": 50,
                "is_published": True
            },
            {
                "title": "Technology and Internet",
                "description": "Modern technology, internet, and digital communication",
                "hsk_level": 4,
                "order": 2,
                "estimated_time": 45,
                "is_published": True
            },
            {
                "title": "Society and Culture",
                "description": "Discuss social issues, traditions, and cultural topics",
                "hsk_level": 4,
                "order": 3,
                "estimated_time": 50,
                "is_published": True
            },
            {
                "title": "Education and Learning",
                "description": "Academic vocabulary, study methods, and education system",
                "hsk_level": 4,
                "order": 4,
                "estimated_time": 45,
                "is_published": True
            },
            {
                "title": "Environment and Nature",
                "description": "Environmental issues, nature, and sustainability",
                "hsk_level": 4,
                "order": 5,
                "estimated_time": 50,
                "is_published": True
            },
            {
                "title": "News and Media",
                "description": "Reading news, understanding media, and current events",
                "hsk_level": 4,
                "order": 6,
                "estimated_time": 45,
                "is_published": True
            },
        ]

        for lesson_data in hsk4_lessons:
            existing = db.query(Lesson).filter(
                Lesson.title == lesson_data["title"],
                Lesson.hsk_level == lesson_data["hsk_level"]
            ).first()
            
            if not existing:
                lesson = Lesson(**lesson_data)
                db.add(lesson)
            else:
                print(f"   [SKIP] Lesson '{lesson_data['title']}' already exists")
        
        db.commit()
        print(f"   [SUCCESS] Created {len(hsk4_lessons)} HSK 4 lessons")

        # Summary
        print("\n" + "=" * 80)
        print("[SUCCESS] All HSK 2, 3, 4 lessons created!")
        print("=" * 80)
        
        # Count lessons by level
        hsk2_count = db.query(Lesson).filter(Lesson.hsk_level == 2).count()
        hsk3_count = db.query(Lesson).filter(Lesson.hsk_level == 3).count()
        hsk4_count = db.query(Lesson).filter(Lesson.hsk_level == 4).count()
        
        print("\nLesson Summary:")
        print(f"   - HSK 1: {db.query(Lesson).filter(Lesson.hsk_level == 1).count()} lessons")
        print(f"   - HSK 2: {hsk2_count} lessons")
        print(f"   - HSK 3: {hsk3_count} lessons")
        print(f"   - HSK 4: {hsk4_count} lessons")
        print(f"   - Total: {db.query(Lesson).count()} lessons")
        
        print("\nTest APIs:")
        print("   curl http://localhost:8000/api/lessons?hsk_level=2")
        print("   curl http://localhost:8000/api/lessons?hsk_level=3")
        print("   curl http://localhost:8000/api/lessons?hsk_level=4")
        print("=" * 80)

    except Exception as e:
        print(f"\n[ERROR] Error seeding lessons: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()

    finally:
        db.close()

if __name__ == "__main__":
    seed_hsk234_lessons()