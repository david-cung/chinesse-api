from sqlalchemy.orm import Session
from database.database import SessionLocal, engine, Base
from models.user import User
from models.character import Character
from models.lesson import Lesson
from models.progress import DailyMission
from utils.auth import get_password_hash


def seed_database():
    db = SessionLocal()

    try:
        print("🛠️ Resetting database tables...")

        # Drop before create (IMPORTANT: avoids FK constraint errors)
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        print("🌱 Starting database seeding...")

        # Seed Characters
        print("📝 Seeding characters...")
        characters_data = [
            {"character": "爱", "pinyin": "ài", "meaning": "love", "hsk_level": 1, "audio_url": "/audio/ai.mp3"},
            {"character": "你", "pinyin": "nǐ", "meaning": "you", "hsk_level": 1, "audio_url": "/audio/ni.mp3"},
            {"character": "好", "pinyin": "hǎo", "meaning": "good", "hsk_level": 1, "audio_url": "/audio/hao.mp3"},
            {"character": "我", "pinyin": "wǒ", "meaning": "I/me", "hsk_level": 1, "audio_url": "/audio/wo.mp3"},
            {"character": "的", "pinyin": "de", "meaning": "of", "hsk_level": 1, "audio_url": "/audio/de.mp3"},
            {"character": "是", "pinyin": "shì", "meaning": "is/am/are", "hsk_level": 1, "audio_url": "/audio/shi.mp3"},
            {"character": "不", "pinyin": "bù", "meaning": "no/not", "hsk_level": 1, "audio_url": "/audio/bu.mp3"},
            {"character": "在", "pinyin": "zài", "meaning": "at/in/on", "hsk_level": 1, "audio_url": "/audio/zai.mp3"},
            {"character": "有", "pinyin": "yǒu", "meaning": "to have", "hsk_level": 1, "audio_url": "/audio/you.mp3"},
            {"character": "人", "pinyin": "rén", "meaning": "person", "hsk_level": 1, "audio_url": "/audio/ren.mp3"},
        ]

        for char_data in characters_data:
            db.add(Character(**char_data))
        db.commit()
        print(f"✅ Added {len(characters_data)} characters")

        # Seed Lessons
        print("📚 Seeding lessons...")
        lessons_data = [
            {
                "title": "Basic Greetings",
                "description": "Learn essential Chinese greetings and introductions",
                "hsk_level": 1,
                "order": 1
            },
            {
                "title": "Self Introduction",
                "description": "Introduce yourself and ask basic questions",
                "hsk_level": 1,
                "order": 2
            },
            {
                "title": "Numbers and Counting",
                "description": "Learn to count and use numbers in Chinese",
                "hsk_level": 1,
                "order": 3
            },
            {
                "title": "Family Members",
                "description": "Vocabulary for family relationships",
                "hsk_level": 1,
                "order": 4
            },
        ]

        for lesson_data in lessons_data:
            db.add(Lesson(**lesson_data))
        db.commit()
        print(f"✅ Added {len(lessons_data)} lessons")

        # Seed Daily Missions
        print("🎯 Seeding daily missions...")
        missions_data = [
            {
                "title": "Learn 10 new words",
                "description": "Complete 10 character exercises",
                "target": 10,
                "reward_xp": 50
            },
            {
                "title": "Complete 1 lesson",
                "description": "Finish at least one full lesson",
                "target": 1,
                "reward_xp": 100
            },
            {
                "title": "Practice pronunciation",
                "description": "Listen to 20 audio pronunciations",
                "target": 20,
                "reward_xp": 30
            },
            {
                "title": "Daily practice",
                "description": "Practice for at least 15 minutes",
                "target": 15,
                "reward_xp": 40
            },
        ]

        for mission_data in missions_data:
            db.add(DailyMission(**mission_data))
        db.commit()
        print(f"✅ Added {len(missions_data)} daily missions")

        # Create demo user
        print("👤 Creating demo user...")
        demo_user = User(
            username="demo",
            email="demo@example.com",
            hashed_password=get_password_hash("demo123"),   # safe with new hashing
            xp=250,
            level=3,
            streak=5,
            gems=100
        )
        db.add(demo_user)
        db.commit()
        print("✅ Created demo user (email: demo@example.com, password: demo123)")

        # Summary
        print("\n🎉 Database seeded successfully!")
        print("\n📊 Summary:")
        print(f"   - Characters: {len(characters_data)}")
        print(f"   - Lessons: {len(lessons_data)}")
        print(f"   - Missions: {len(missions_data)}")
        print(f"   - Users: 1 (demo)")

    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
