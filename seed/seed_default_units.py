"""
Seed script to create default units for all existing lessons.
Each lesson will have 4 units: vocabulary, listening, speaking, exercise
"""
from database.database import SessionLocal
from models.lesson import Lesson
from models.unit import Unit


def seed_default_units():
    db = SessionLocal()
    
    try:
        # Get all lessons
        lessons = db.query(Lesson).all()
        print(f"📚 Found {len(lessons)} lessons")
        
        created_count = 0
        
        for lesson in lessons:
            # Check if lesson already has units
            existing_units = db.query(Unit).filter(Unit.lesson_id == lesson.id).count()
            
            if existing_units > 0:
                print(f"⏭️  Skipping: {lesson.title} (already has {existing_units} units)")
                continue
            
            # Create 4 default units for each lesson
            default_units = [
                {"type": "vocabulary", "title": "Học từ vựng", "order": 1, "duration_minutes": 5},
                {"type": "listening", "title": "Nghe hiểu", "order": 2, "duration_minutes": 5},
                {"type": "speaking", "title": "Luyện nói", "order": 3, "duration_minutes": 5},
                {"type": "exercise", "title": "Bài tập", "order": 4, "duration_minutes": 5},
            ]
            
            for unit_data in default_units:
                unit = Unit(
                    lesson_id=lesson.id,
                    type=unit_data["type"],
                    title=unit_data["title"],
                    order=unit_data["order"],
                    duration_minutes=unit_data["duration_minutes"]
                )
                db.add(unit)
                created_count += 1
            
            print(f"✅ Created 4 units for: {lesson.title}")
        
        db.commit()
        print(f"\n🎉 Done! Created {created_count} units")
        
        # Show total
        total = db.query(Unit).count()
        print(f"📦 Total units in database: {total}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_default_units()
