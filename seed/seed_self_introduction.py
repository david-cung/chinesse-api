# seed_self_introduction.py
import sys
sys.path.append('.')

from sqlalchemy.orm import Session
from database.database import SessionLocal, engine
from models.lesson import (
    Lesson, 
    Vocabulary, 
    LessonObjective, 
    GrammarPoint, 
    GrammarExample, 
    Exercise
)
from models.character import Character

def seed_self_introduction():
    """Seed detailed data for Self Introduction lesson (Lesson 2)"""
    db = SessionLocal()

    try:
        print("=" * 80)
        print("Seeding Self Introduction Lesson Details...")
        print("=" * 80)

        # Find or create Lesson 2
        lesson2 = db.query(Lesson).filter(Lesson.order == 2).first()
        
        if not lesson2:
            print("[INFO] Creating Self Introduction lesson...")
            lesson2 = Lesson(
                title="Self Introduction",
                description="Introduce yourself and ask basic questions",
                hsk_level=1,
                order=2,
                estimated_time=30,
                is_published=True
            )
            db.add(lesson2)
            db.flush()
        else:
            print(f"[INFO] Found existing lesson: {lesson2.title}")

        # 1. Add/Link Characters
        print("\n[1/5] Adding characters...")
        characters_data = [
            {"character": "我", "pinyin": "wǒ", "meaning": "I/me", "hsk_level": 1, "stroke_count": 7},
            {"character": "是", "pinyin": "shì", "meaning": "is/am/are", "hsk_level": 1, "stroke_count": 9},
            {"character": "叫", "pinyin": "jiào", "meaning": "to be called", "hsk_level": 1, "stroke_count": 5},
            {"character": "什", "pinyin": "shén", "meaning": "what", "hsk_level": 1, "stroke_count": 4},
            {"character": "么", "pinyin": "me", "meaning": "question particle", "hsk_level": 1, "stroke_count": 3},
            {"character": "名", "pinyin": "míng", "meaning": "name", "hsk_level": 1, "stroke_count": 6},
            {"character": "字", "pinyin": "zì", "meaning": "character/word", "hsk_level": 1, "stroke_count": 6},
            {"character": "来", "pinyin": "lái", "meaning": "to come", "hsk_level": 1, "stroke_count": 7},
            {"character": "从", "pinyin": "cóng", "meaning": "from", "hsk_level": 1, "stroke_count": 4},
            {"character": "哪", "pinyin": "nǎ", "meaning": "which/where", "hsk_level": 1, "stroke_count": 9},
        ]

        lesson2.characters.clear()  # Clear existing relationships
        for char_data in characters_data:
            # Check if character exists
            char = db.query(Character).filter(Character.character == char_data["character"]).first()
            if not char:
                char = Character(**char_data)
                db.add(char)
                db.flush()
            lesson2.characters.append(char)
        
        db.flush()
        print(f"   [SUCCESS] Linked {len(characters_data)} characters")

        # 2. Add Vocabulary
        print("\n[2/5] Adding vocabulary...")
        
        # Clear existing vocabulary
        lesson2.vocabularies.clear()
        
        vocab_items = [
            {
                "word": "我叫", 
                "pinyin": "wǒ jiào", 
                "meaning": "my name is", 
                "example": "我叫李明。(Wǒ jiào Lǐ Míng.) - My name is Li Ming.",
                "hsk_level": 1
            },
            {
                "word": "名字", 
                "pinyin": "míng zi", 
                "meaning": "name", 
                "example": "你叫什么名字？(Nǐ jiào shén me míng zi?) - What's your name?",
                "hsk_level": 1
            },
            {
                "word": "什么", 
                "pinyin": "shén me", 
                "meaning": "what", 
                "example": "这是什么？(Zhè shì shén me?) - What is this?",
                "hsk_level": 1
            },
            {
                "word": "我是", 
                "pinyin": "wǒ shì", 
                "meaning": "I am", 
                "example": "我是学生。(Wǒ shì xué shēng.) - I am a student.",
                "hsk_level": 1
            },
            {
                "word": "来自", 
                "pinyin": "lái zì", 
                "meaning": "come from", 
                "example": "我来自中国。(Wǒ lái zì Zhōng guó.) - I come from China.",
                "hsk_level": 1
            },
            {
                "word": "哪里", 
                "pinyin": "nǎ lǐ", 
                "meaning": "where", 
                "example": "你来自哪里？(Nǐ lái zì nǎ lǐ?) - Where are you from?",
                "hsk_level": 1
            },
            {
                "word": "学生", 
                "pinyin": "xué shēng", 
                "meaning": "student", 
                "example": "他是学生。(Tā shì xué shēng.) - He is a student.",
                "hsk_level": 1
            },
            {
                "word": "老师", 
                "pinyin": "lǎo shī", 
                "meaning": "teacher", 
                "example": "她是老师。(Tā shì lǎo shī.) - She is a teacher.",
                "hsk_level": 1
            },
        ]

        for vocab_data in vocab_items:
            vocab = Vocabulary(**vocab_data)
            db.add(vocab)
            db.flush()
            lesson2.vocabularies.append(vocab)
        
        print(f"   [SUCCESS] Added {len(vocab_items)} vocabulary items")

        # 3. Add Objectives
        print("\n[3/5] Adding objectives...")
        
        # Delete existing objectives
        db.query(LessonObjective).filter(LessonObjective.lesson_id == lesson2.id).delete()
        
        objectives = [
            "Học cách tự giới thiệu bản thân bằng tiếng Trung",
            "Nắm vững cách tự giới thiệu bản thân",
            "Phát âm chuẩn các Hán tự cơ bản",
            "Hỏi và trả lời về tên và xuất xứ",
            "Sử dụng câu hỏi 'Bạn tên là gì?' và 'Bạn đến từ đâu?'",
        ]
        
        for idx, obj_text in enumerate(objectives):
            obj = LessonObjective(
                lesson_id=lesson2.id, 
                objective=obj_text, 
                order=idx
            )
            db.add(obj)
        
        print(f"   [SUCCESS] Added {len(objectives)} objectives")

        # 4. Add Grammar Points
        print("\n[4/5] Adding grammar points...")
        
        # Delete existing grammar points and examples
        db.query(GrammarExample).filter(
            GrammarExample.grammar_point_id.in_(
                db.query(GrammarPoint.id).filter(GrammarPoint.lesson_id == lesson2.id)
            )
        ).delete(synchronize_session=False)
        db.query(GrammarPoint).filter(GrammarPoint.lesson_id == lesson2.id).delete()
        
        # Grammar Point 1: 我叫...
        grammar1 = GrammarPoint(
            lesson_id=lesson2.id,
            title="我叫... (Wǒ jiào...) - Giới thiệu tên",
            explanation="Sử dụng '我叫' + tên để giới thiệu tên của bạn. Đây là cách phổ biến nhất để nói 'Tôi tên là...'",
            order=1
        )
        db.add(grammar1)
        db.flush()

        examples1 = [
            {
                "example": "我叫王明。(Wǒ jiào Wáng Míng.)",
                "translation": "Tôi tên là Wang Ming.",
                "order": 1
            },
            {
                "example": "你叫什么名字？(Nǐ jiào shén me míng zi?)",
                "translation": "Bạn tên là gì?",
                "order": 2
            },
            {
                "example": "她叫李娜。(Tā jiào Lǐ Nà.)",
                "translation": "Cô ấy tên là Li Na.",
                "order": 3
            },
        ]

        for ex_data in examples1:
            ex = GrammarExample(grammar_point_id=grammar1.id, **ex_data)
            db.add(ex)

        # Grammar Point 2: 我是...
        grammar2 = GrammarPoint(
            lesson_id=lesson2.id,
            title="我是... (Wǒ shì...) - Giới thiệu nghề nghiệp/danh tính",
            explanation="Sử dụng '我是' + nghề nghiệp/danh tính để giới thiệu về bản thân. '是' có nghĩa là 'là/am/is'.",
            order=2
        )
        db.add(grammar2)
        db.flush()

        examples2 = [
            {
                "example": "我是学生。(Wǒ shì xué shēng.)",
                "translation": "Tôi là sinh viên.",
                "order": 1
            },
            {
                "example": "他是老师。(Tā shì lǎo shī.)",
                "translation": "Anh ấy là giáo viên.",
                "order": 2
            },
            {
                "example": "你是医生吗？(Nǐ shì yī shēng ma?)",
                "translation": "Bạn có phải là bác sĩ không?",
                "order": 3
            },
        ]

        for ex_data in examples2:
            ex = GrammarExample(grammar_point_id=grammar2.id, **ex_data)
            db.add(ex)

        # Grammar Point 3: 来自...
        grammar3 = GrammarPoint(
            lesson_id=lesson2.id,
            title="我来自... (Wǒ lái zì...) - Nói về xuất xứ",
            explanation="Sử dụng '来自' để nói về nơi bạn đến từ. '来自' có nghĩa là 'đến từ'.",
            order=3
        )
        db.add(grammar3)
        db.flush()

        examples3 = [
            {
                "example": "我来自越南。(Wǒ lái zì Yuè nán.)",
                "translation": "Tôi đến từ Việt Nam.",
                "order": 1
            },
            {
                "example": "你来自哪里？(Nǐ lái zì nǎ lǐ?)",
                "translation": "Bạn đến từ đâu?",
                "order": 2
            },
            {
                "example": "她来自北京。(Tā lái zì Běi jīng.)",
                "translation": "Cô ấy đến từ Bắc Kinh.",
                "order": 3
            },
        ]

        for ex_data in examples3:
            ex = GrammarExample(grammar_point_id=grammar3.id, **ex_data)
            db.add(ex)

        print(f"   [SUCCESS] Added 3 grammar points with examples")

        # 5. Add Exercises
        print("\n[5/5] Adding exercises...")
        
        # Delete existing exercises
        db.query(Exercise).filter(Exercise.lesson_id == lesson2.id).delete()
        
        exercises = [
            {
                "type": "multiple_choice",
                "question": "Làm thế nào để nói 'Tôi tên là...' bằng tiếng Trung?",
                "answer": "我叫",
                "options": '["我叫", "我是", "你好", "再见"]',
                "order": 1
            },
            {
                "type": "multiple_choice",
                "question": "Từ nào có nghĩa là 'tên'?",
                "answer": "名字",
                "options": '["名字", "学生", "老师", "什么"]',
                "order": 2
            },
            {
                "type": "translation",
                "question": "Dịch sang tiếng Trung: 'Bạn tên là gì?'",
                "answer": "你叫什么名字？",
                "options": '[]',
                "order": 3
            },
            {
                "type": "multiple_choice",
                "question": "'来自' có nghĩa là gì?",
                "answer": "đến từ",
                "options": '["đến từ", "tên là", "là", "sinh viên"]',
                "order": 4
            },
            {
                "type": "fill_blank",
                "question": "Điền từ thích hợp: 我___学生。(Tôi là sinh viên)",
                "answer": "是",
                "options": '["是", "叫", "来", "什么"]',
                "order": 5
            },
            {
                "type": "translation",
                "question": "Dịch sang tiếng Trung: 'Tôi đến từ Việt Nam'",
                "answer": "我来自越南。",
                "options": '[]',
                "order": 6
            },
            {
                "type": "multiple_choice",
                "question": "Cách hỏi 'Bạn đến từ đâu?' là gì?",
                "answer": "你来自哪里？",
                "options": '["你来自哪里？", "你叫什么名字？", "你好吗？", "你是谁？"]',
                "order": 7
            },
            {
                "type": "fill_blank",
                "question": "Điền từ: 你___什么名字？(Bạn tên là gì?)",
                "answer": "叫",
                "options": '["叫", "是", "来", "从"]',
                "order": 8
            },
        ]

        for ex_data in exercises:
            ex = Exercise(lesson_id=lesson2.id, **ex_data)
            db.add(ex)
        
        print(f"   [SUCCESS] Added {len(exercises)} exercises")

        # Commit all changes
        db.commit()

        # Verification
        print("\n" + "=" * 80)
        print("VERIFICATION - Self Introduction Lesson Details:")
        print("=" * 80)
        lesson_check = db.query(Lesson).filter(Lesson.id == lesson2.id).first()
        print(f"Title: {lesson_check.title}")
        print(f"  - Characters: {len(lesson_check.characters)}")
        print(f"  - Vocabulary: {len(lesson_check.vocabularies)}")
        print(f"  - Objectives: {len(lesson_check.objectives)}")
        print(f"  - Grammar Points: {len(lesson_check.grammar_points)}")
        print(f"  - Exercises: {len(lesson_check.exercises)}")

        print("\n" + "=" * 80)
        print("[SUCCESS] Self Introduction lesson seeded successfully!")
        print("=" * 80)
        print("\nTest API:")
        print(f"   curl http://localhost:8000/api/lessons/{lesson2.id}")
        print("=" * 80)

    except Exception as e:
        print(f"\n[ERROR] Error seeding Self Introduction: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()

    finally:
        db.close()

if __name__ == "__main__":
    seed_self_introduction()