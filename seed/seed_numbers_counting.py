# seed_numbers_counting.py
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

def seed_numbers_counting():
    """Seed detailed data for Numbers and Counting lesson (Lesson 3)"""
    db = SessionLocal()

    try:
        print("=" * 80)
        print("Seeding Numbers and Counting Lesson Details...")
        print("=" * 80)

        # Find or create Lesson 3
        lesson3 = db.query(Lesson).filter(Lesson.order == 3).first()
        
        if not lesson3:
            print("[INFO] Creating Numbers and Counting lesson...")
            lesson3 = Lesson(
                title="Numbers and Counting",
                description="Learn to count and use numbers in Chinese",
                hsk_level=1,
                order=3,
                estimated_time=35,
                is_published=True
            )
            db.add(lesson3)
            db.flush()
        else:
            print(f"[INFO] Found existing lesson: {lesson3.title}")

        # 1. Add/Link Characters
        print("\n[1/5] Adding characters...")
        characters_data = [
            {"character": "一", "pinyin": "yī", "meaning": "one", "hsk_level": 1, "stroke_count": 1},
            {"character": "二", "pinyin": "èr", "meaning": "two", "hsk_level": 1, "stroke_count": 2},
            {"character": "三", "pinyin": "sān", "meaning": "three", "hsk_level": 1, "stroke_count": 3},
            {"character": "四", "pinyin": "sì", "meaning": "four", "hsk_level": 1, "stroke_count": 5},
            {"character": "五", "pinyin": "wǔ", "meaning": "five", "hsk_level": 1, "stroke_count": 4},
            {"character": "六", "pinyin": "liù", "meaning": "six", "hsk_level": 1, "stroke_count": 4},
            {"character": "七", "pinyin": "qī", "meaning": "seven", "hsk_level": 1, "stroke_count": 2},
            {"character": "八", "pinyin": "bā", "meaning": "eight", "hsk_level": 1, "stroke_count": 2},
            {"character": "九", "pinyin": "jiǔ", "meaning": "nine", "hsk_level": 1, "stroke_count": 2},
            {"character": "十", "pinyin": "shí", "meaning": "ten", "hsk_level": 1, "stroke_count": 2},
            {"character": "百", "pinyin": "bǎi", "meaning": "hundred", "hsk_level": 1, "stroke_count": 6},
            {"character": "千", "pinyin": "qiān", "meaning": "thousand", "hsk_level": 1, "stroke_count": 3},
        ]

        lesson3.characters.clear()
        for char_data in characters_data:
            char = db.query(Character).filter(Character.character == char_data["character"]).first()
            if not char:
                char = Character(**char_data)
                db.add(char)
                db.flush()
            lesson3.characters.append(char)
        
        db.flush()
        print(f"   [SUCCESS] Linked {len(characters_data)} characters")

        # 2. Add Vocabulary
        print("\n[2/5] Adding vocabulary...")
        lesson3.vocabularies.clear()
        
        vocab_items = [
            {
                "word": "一", 
                "pinyin": "yī", 
                "meaning": "one", 
                "example": "一个人 (yī gè rén) - one person",
                "hsk_level": 1
            },
            {
                "word": "二", 
                "pinyin": "èr", 
                "meaning": "two", 
                "example": "二月 (èr yuè) - February",
                "hsk_level": 1
            },
            {
                "word": "三", 
                "pinyin": "sān", 
                "meaning": "three", 
                "example": "三天 (sān tiān) - three days",
                "hsk_level": 1
            },
            {
                "word": "四", 
                "pinyin": "sì", 
                "meaning": "four", 
                "example": "四月 (sì yuè) - April",
                "hsk_level": 1
            },
            {
                "word": "五", 
                "pinyin": "wǔ", 
                "meaning": "five", 
                "example": "五个 (wǔ gè) - five (items)",
                "hsk_level": 1
            },
            {
                "word": "六", 
                "pinyin": "liù", 
                "meaning": "six", 
                "example": "六点 (liù diǎn) - six o'clock",
                "hsk_level": 1
            },
            {
                "word": "七", 
                "pinyin": "qī", 
                "meaning": "seven", 
                "example": "七天 (qī tiān) - seven days",
                "hsk_level": 1
            },
            {
                "word": "八", 
                "pinyin": "bā", 
                "meaning": "eight", 
                "example": "八月 (bā yuè) - August",
                "hsk_level": 1
            },
            {
                "word": "九", 
                "pinyin": "jiǔ", 
                "meaning": "nine", 
                "example": "九点 (jiǔ diǎn) - nine o'clock",
                "hsk_level": 1
            },
            {
                "word": "十", 
                "pinyin": "shí", 
                "meaning": "ten", 
                "example": "十个 (shí gè) - ten (items)",
                "hsk_level": 1
            },
            {
                "word": "多少", 
                "pinyin": "duō shao", 
                "meaning": "how many/how much", 
                "example": "多少钱？(duō shao qián?) - How much money?",
                "hsk_level": 1
            },
            {
                "word": "几", 
                "pinyin": "jǐ", 
                "meaning": "how many (small number)", 
                "example": "几个人？(jǐ gè rén?) - How many people?",
                "hsk_level": 1
            },
        ]

        for vocab_data in vocab_items:
            vocab = Vocabulary(**vocab_data)
            db.add(vocab)
            db.flush()
            lesson3.vocabularies.append(vocab)
        
        print(f"   [SUCCESS] Added {len(vocab_items)} vocabulary items")

        # 3. Add Objectives
        print("\n[3/5] Adding objectives...")
        db.query(LessonObjective).filter(LessonObjective.lesson_id == lesson3.id).delete()
        
        objectives = [
            "Học đếm từ 1 đến 10 bằng tiếng Trung",
            "Nắm vững cách phát âm các số",
            "Hiểu cách kết hợp số để tạo số lớn hơn (11-99)",
            "Sử dụng 'đo shao' và 'jǐ' để hỏi số lượng",
            "Áp dụng số vào các tình huống thực tế",
        ]
        
        for idx, obj_text in enumerate(objectives):
            obj = LessonObjective(
                lesson_id=lesson3.id, 
                objective=obj_text, 
                order=idx
            )
            db.add(obj)
        
        print(f"   [SUCCESS] Added {len(objectives)} objectives")

        # 4. Add Grammar Points
        print("\n[4/5] Adding grammar points...")
        
        db.query(GrammarExample).filter(
            GrammarExample.grammar_point_id.in_(
                db.query(GrammarPoint.id).filter(GrammarPoint.lesson_id == lesson3.id)
            )
        ).delete(synchronize_session=False)
        db.query(GrammarPoint).filter(GrammarPoint.lesson_id == lesson3.id).delete()
        
        # Grammar Point 1: Đếm cơ bản 1-10
        grammar1 = GrammarPoint(
            lesson_id=lesson3.id,
            title="Đếm từ 1 đến 10",
            explanation="Các số từ 1-10 là nền tảng. Học thuộc lòng các số này vì chúng được sử dụng để tạo tất cả các số khác.",
            order=1
        )
        db.add(grammar1)
        db.flush()

        examples1 = [
            {
                "example": "一、二、三、四、五 (yī, èr, sān, sì, wǔ)",
                "translation": "Một, hai, ba, bốn, năm",
                "order": 1
            },
            {
                "example": "六、七、八、九、十 (liù, qī, bā, jiǔ, shí)",
                "translation": "Sáu, bảy, tám, chín, mười",
                "order": 2
            },
        ]

        for ex_data in examples1:
            ex = GrammarExample(grammar_point_id=grammar1.id, **ex_data)
            db.add(ex)

        # Grammar Point 2: Số 11-99
        grammar2 = GrammarPoint(
            lesson_id=lesson3.id,
            title="Tạo số 11-99",
            explanation="Để tạo số 11-99: Hàng chục + đơn vị. Ví dụ: 十一 (11) = 十(10) + 一(1), 二十三 (23) = 二十(20) + 三(3).",
            order=2
        )
        db.add(grammar2)
        db.flush()

        examples2 = [
            {
                "example": "十一 (shí yī)",
                "translation": "11 (mười một)",
                "order": 1
            },
            {
                "example": "二十 (èr shí)",
                "translation": "20 (hai mươi)",
                "order": 2
            },
            {
                "example": "三十五 (sān shí wǔ)",
                "translation": "35 (ba mươi lăm)",
                "order": 3
            },
            {
                "example": "九十九 (jiǔ shí jiǔ)",
                "translation": "99 (chín mươi chín)",
                "order": 4
            },
        ]

        for ex_data in examples2:
            ex = GrammarExample(grammar_point_id=grammar2.id, **ex_data)
            db.add(ex)

        # Grammar Point 3: Hỏi số lượng
        grammar3 = GrammarPoint(
            lesson_id=lesson3.id,
            title="Hỏi 'Bao nhiêu?' - 多少 vs 几",
            explanation="Dùng '几' (jǐ) cho số nhỏ (dưới 10), dùng '多少' (duō shao) cho số lớn hoặc không biết khoảng.",
            order=3
        )
        db.add(grammar3)
        db.flush()

        examples3 = [
            {
                "example": "你有几个苹果？(nǐ yǒu jǐ gè píng guǒ?)",
                "translation": "Bạn có mấy quả táo? (số nhỏ)",
                "order": 1
            },
            {
                "example": "这个多少钱？(zhè ge duō shao qián?)",
                "translation": "Cái này bao nhiêu tiền? (số lớn/không biết)",
                "order": 2
            },
            {
                "example": "现在几点？(xiàn zài jǐ diǎn?)",
                "translation": "Bây giờ mấy giờ? (giờ dùng 几)",
                "order": 3
            },
        ]

        for ex_data in examples3:
            ex = GrammarExample(grammar_point_id=grammar3.id, **ex_data)
            db.add(ex)

        print(f"   [SUCCESS] Added 3 grammar points with examples")

        # 5. Add Exercises
        print("\n[5/5] Adding exercises...")
        db.query(Exercise).filter(Exercise.lesson_id == lesson3.id).delete()
        
        exercises = [
            {
                "type": "multiple_choice",
                "question": "Số '5' trong tiếng Trung là gì?",
                "answer": "五",
                "options": '["五", "四", "六", "七"]',
                "order": 1
            },
            {
                "type": "multiple_choice",
                "question": "Làm thế nào để nói '8' bằng tiếng Trung?",
                "answer": "八",
                "options": '["八", "七", "九", "六"]',
                "order": 2
            },
            {
                "type": "translation",
                "question": "Dịch sang tiếng Trung: 'Mười'",
                "answer": "十",
                "options": '[]',
                "order": 3
            },
            {
                "type": "multiple_choice",
                "question": "Số '23' viết như thế nào?",
                "answer": "二十三",
                "options": '["二十三", "三十二", "十二三", "二三十"]',
                "order": 4
            },
            {
                "type": "fill_blank",
                "question": "Điền số: 一、二、___、四、五",
                "answer": "三",
                "options": '["三", "六", "七", "八"]',
                "order": 5
            },
            {
                "type": "multiple_choice",
                "question": "'多少' có nghĩa là gì?",
                "answer": "bao nhiêu",
                "options": '["bao nhiêu", "mấy", "một", "hai"]',
                "order": 6
            },
            {
                "type": "translation",
                "question": "Số '15' trong tiếng Trung",
                "answer": "十五",
                "options": '[]',
                "order": 7
            },
            {
                "type": "multiple_choice",
                "question": "Khi hỏi 'Mấy giờ rồi?', dùng từ nào?",
                "answer": "几",
                "options": '["几", "多少", "什么", "哪"]',
                "order": 8
            },
            {
                "type": "fill_blank",
                "question": "Số 100: 一___",
                "answer": "百",
                "options": '["百", "千", "十", "万"]',
                "order": 9
            },
            {
                "type": "multiple_choice",
                "question": "Số '99' viết như thế nào?",
                "answer": "九十九",
                "options": '["九十九", "九九", "十九九", "九九十"]',
                "order": 10
            },
        ]

        for ex_data in exercises:
            ex = Exercise(lesson_id=lesson3.id, **ex_data)
            db.add(ex)
        
        print(f"   [SUCCESS] Added {len(exercises)} exercises")

        # Commit all changes
        db.commit()

        # Verification
        print("\n" + "=" * 80)
        print("VERIFICATION - Numbers and Counting Lesson Details:")
        print("=" * 80)
        lesson_check = db.query(Lesson).filter(Lesson.id == lesson3.id).first()
        print(f"Title: {lesson_check.title}")
        print(f"  - Characters: {len(lesson_check.characters)}")
        print(f"  - Vocabulary: {len(lesson_check.vocabularies)}")
        print(f"  - Objectives: {len(lesson_check.objectives)}")
        print(f"  - Grammar Points: {len(lesson_check.grammar_points)}")
        print(f"  - Exercises: {len(lesson_check.exercises)}")

        print("\n" + "=" * 80)
        print("[SUCCESS] Numbers and Counting lesson seeded successfully!")
        print("=" * 80)
        print("\nTest API:")
        print(f"   curl http://localhost:8000/api/lessons/{lesson3.id}")
        print("=" * 80)

    except Exception as e:
        print(f"\n[ERROR] Error seeding Numbers and Counting: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()

    finally:
        db.close()

if __name__ == "__main__":
    seed_numbers_counting()