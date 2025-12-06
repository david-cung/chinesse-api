# seed_database.py
import sys
sys.path.append('.')

from sqlalchemy.orm import Session
from database.database import SessionLocal, engine, Base
from models.user import User
from models.character import Character
from models.progress import DailyMission
from utils.auth import get_password_hash

# Import ALL lesson models (including association tables)
from models.lesson import (
    Lesson, 
    Vocabulary, 
    LessonObjective, 
    GrammarPoint, 
    GrammarExample, 
    Exercise,
    lesson_characters,      # Association table
    lesson_vocabulary       # Association table
)

def seed_database():
    db = SessionLocal()

    try:
        print("=" * 80)
        print("Resetting database tables...")
        print("=" * 80)

        # Drop before create (IMPORTANT: avoids FK constraint errors)
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        print("\n[SUCCESS] Tables created!")
        print("\nStarting database seeding...")
        print("=" * 80)

        # 1. Seed Characters FIRST
        print("\n[1/5] Seeding characters...")
        characters_data = [
            {"character": "爱", "pinyin": "ài", "meaning": "love", "hsk_level": 1, "stroke_count": 10, "audio_url": "/audio/ai.mp3"},
            {"character": "你", "pinyin": "nǐ", "meaning": "you", "hsk_level": 1, "stroke_count": 7, "audio_url": "/audio/ni.mp3"},
            {"character": "好", "pinyin": "hǎo", "meaning": "good", "hsk_level": 1, "stroke_count": 6, "audio_url": "/audio/hao.mp3"},
            {"character": "我", "pinyin": "wǒ", "meaning": "I/me", "hsk_level": 1, "stroke_count": 7, "audio_url": "/audio/wo.mp3"},
            {"character": "的", "pinyin": "de", "meaning": "of", "hsk_level": 1, "stroke_count": 8, "audio_url": "/audio/de.mp3"},
            {"character": "是", "pinyin": "shì", "meaning": "is/am/are", "hsk_level": 1, "stroke_count": 9, "audio_url": "/audio/shi.mp3"},
            {"character": "不", "pinyin": "bù", "meaning": "no/not", "hsk_level": 1, "stroke_count": 4, "audio_url": "/audio/bu.mp3"},
            {"character": "在", "pinyin": "zài", "meaning": "at/in/on", "hsk_level": 1, "stroke_count": 6, "audio_url": "/audio/zai.mp3"},
            {"character": "有", "pinyin": "yǒu", "meaning": "to have", "hsk_level": 1, "stroke_count": 6, "audio_url": "/audio/you.mp3"},
            {"character": "人", "pinyin": "rén", "meaning": "person", "hsk_level": 1, "stroke_count": 2, "audio_url": "/audio/ren.mp3"},
        ]

        created_characters = []
        for char_data in characters_data:
            char = Character(**char_data)
            db.add(char)
            created_characters.append(char)
        db.flush()  # Flush to get IDs
        print(f"   [SUCCESS] Added {len(characters_data)} characters")

        # 2. Create Lesson 1 with FULL details
        print("\n[2/5] Creating Lesson 1: Basic Greetings (with details)...")
        lesson1 = Lesson(
            title="Basic Greetings",
            description="Learn essential Chinese greetings and introductions",
            hsk_level=1,
            order=1,
            estimated_time=25,
            is_published=True
        )
        db.add(lesson1)
        db.flush()

        # Link characters to lesson 1 (using the relationship)
        lesson1.characters.append(created_characters[1])  # 你
        lesson1.characters.append(created_characters[2])  # 好
        lesson1.characters.append(created_characters[3])  # 我
        lesson1.characters.append(created_characters[5])  # 是
        db.flush()
        print(f"   [INFO] Linked 4 characters to Lesson 1")

        # Add vocabulary items
        print("   [INFO] Adding vocabulary...")
        vocab_items = [
            {"word": "你好", "pinyin": "nǐ hǎo", "meaning": "hello", 
             "example": "你好！很高兴认识你。", "hsk_level": 1},
            {"word": "早上好", "pinyin": "zǎo shang hǎo", "meaning": "good morning",
             "example": "早上好！今天天气很好。", "hsk_level": 1},
            {"word": "晚安", "pinyin": "wǎn ān", "meaning": "good night",
             "example": "晚安，明天见！", "hsk_level": 1},
            {"word": "再见", "pinyin": "zài jiàn", "meaning": "goodbye",
             "example": "再见！路上小心。", "hsk_level": 1},
        ]

        for vocab_data in vocab_items:
            vocab = Vocabulary(**vocab_data)
            db.add(vocab)
            db.flush()
            lesson1.vocabularies.append(vocab)  # Link to lesson
        print(f"   [SUCCESS] Added {len(vocab_items)} vocabulary items")

        # Add objectives
        objectives = [
            "Học cách chào hỏi cơ bản bằng tiếng Trung",
            "Nắm vững cách tự giới thiệu bản thân",
            "Phát âm chuẩn các Hán tự cơ bản",
        ]
        for idx, obj_text in enumerate(objectives):
            obj = LessonObjective(lesson_id=lesson1.id, objective=obj_text, order=idx)
            db.add(obj)
        print(f"   [SUCCESS] Added {len(objectives)} objectives")

        # Add grammar point
        grammar1 = GrammarPoint(
            lesson_id=lesson1.id,
            title="你好 - Cách chào hỏi cơ bản",
            explanation="'你好' (nǐ hǎo) là cách chào hỏi phổ biến nhất trong tiếng Trung.",
            order=1
        )
        db.add(grammar1)
        db.flush()

        # Add grammar examples
        grammar_ex1 = GrammarExample(
            grammar_point_id=grammar1.id,
            example="你好！(Nǐ hǎo!)",
            translation="Xin chào!",
            order=1
        )
        db.add(grammar_ex1)
        print(f"   [SUCCESS] Added 1 grammar point with examples")

        # Add exercises
        exercise1 = Exercise(
            lesson_id=lesson1.id,
            type="multiple_choice",
            question="Làm thế nào để nói 'Xin chào' bằng tiếng Trung?",
            answer="你好",
            options='["你好", "再见", "谢谢", "对不起"]',
            order=1
        )
        db.add(exercise1)
        print(f"   [SUCCESS] Added exercises")

        db.commit()

        # 3. Create other lessons (basic)
        print("\n[3/5] Creating other lessons...")
        other_lessons = [
            {
                "title": "Self Introduction",
                "description": "Introduce yourself and ask basic questions",
                "hsk_level": 1,
                "order": 2,
                "estimated_time": 30,
                "is_published": True
            },
            {
                "title": "Numbers and Counting",
                "description": "Learn to count and use numbers in Chinese",
                "hsk_level": 1,
                "order": 3,
                "estimated_time": 35,
                "is_published": True
            },
            {
                "title": "Family Members",
                "description": "Vocabulary for family relationships",
                "hsk_level": 1,
                "order": 4,
                "estimated_time": 30,
                "is_published": True
            },
        ]

        for lesson_data in other_lessons:
            lesson = Lesson(**lesson_data)
            db.add(lesson)
        db.commit()
        print(f"   [SUCCESS] Added {len(other_lessons)} lessons")

        # 4. Seed Daily Missions
        print("\n[4/5] Seeding daily missions...")
        missions_data = [
            {"title": "Learn 10 new words", "description": "Complete 10 character exercises", "target": 10, "reward_xp": 50},
            {"title": "Complete 1 lesson", "description": "Finish at least one full lesson", "target": 1, "reward_xp": 100},
            {"title": "Practice pronunciation", "description": "Listen to 20 audio pronunciations", "target": 20, "reward_xp": 30},
            {"title": "Daily practice", "description": "Practice for at least 15 minutes", "target": 15, "reward_xp": 40},
        ]

        for mission_data in missions_data:
            db.add(DailyMission(**mission_data))
        db.commit()
        print(f"   [SUCCESS] Added {len(missions_data)} daily missions")

        # 5. Create demo user
        print("\n[5/5] Creating demo user...")
        demo_user = User(
            username="demo",
            email="demo@example.com",
            hashed_password=get_password_hash("demo123"),
            xp=250,
            level=3,
            streak=5,
            gems=100
        )
        db.add(demo_user)
        db.commit()
        print("   [SUCCESS] Created demo user (email: demo@example.com, password: demo123)")

        # Verify lesson 1 data
        print("\n" + "=" * 80)
        print("VERIFICATION - Lesson 1 Details:")
        print("=" * 80)
        lesson_check = db.query(Lesson).filter(Lesson.id == lesson1.id).first()
        print(f"Title: {lesson_check.title}")
        print(f"  - Characters: {len(lesson_check.characters)}")
        print(f"  - Vocabulary: {len(lesson_check.vocabularies)}")
        print(f"  - Objectives: {len(lesson_check.objectives)}")
        print(f"  - Grammar Points: {len(lesson_check.grammar_points)}")
        print(f"  - Exercises: {len(lesson_check.exercises)}")

        # Summary
        print("\n" + "=" * 80)
        print("[SUCCESS] Database seeded successfully!")
        print("=" * 80)
        print("\nSummary:")
        print(f"   - Characters: {len(characters_data)}")
        print(f"   - Lessons: 4 total (Lesson 1 has full details)")
        print(f"   - Daily Missions: {len(missions_data)}")
        print(f"   - Users: 1 (demo)")
        print("\nTest API:")
        print("   curl http://localhost:8000/api/lessons?hsk_level=1")
        print("   curl http://localhost:8000/api/lessons/1")
        print("=" * 80)

    except Exception as e:
        print(f"\n[ERROR] Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
