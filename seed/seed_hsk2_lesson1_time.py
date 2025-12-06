# seed_hsk2_details.py
import sys
sys.path.append('.')

from sqlalchemy.orm import Session
from database.database import SessionLocal, engine
from models.lesson import (
    Lesson, Vocabulary, LessonObjective, GrammarPoint, GrammarExample, Exercise
)
from models.character import Character

def add_characters_to_lesson(db, lesson, characters_data):
    """Helper function to add characters to a lesson"""
    lesson.characters.clear()
    for char_data in characters_data:
        char = db.query(Character).filter(Character.character == char_data["character"]).first()
        if not char:
            char = Character(**char_data)
            db.add(char)
            db.flush()
        lesson.characters.append(char)
    db.flush()

def add_vocabulary_to_lesson(db, lesson, vocab_items):
    """Helper function to add vocabulary to a lesson"""
    lesson.vocabularies.clear()
    for vocab_data in vocab_items:
        vocab = Vocabulary(**vocab_data)
        db.add(vocab)
        db.flush()
        lesson.vocabularies.append(vocab)

def seed_time_and_date(db):
    """Seed Time and Date lesson (HSK 2 - Lesson 1)"""
    print("\n[HSK 2.1] Seeding Time and Date...")
    
    lesson = db.query(Lesson).filter(Lesson.title == "Time and Date", Lesson.hsk_level == 2).first()
    if not lesson:
        print("   [ERROR] Lesson not found. Run seed_hsk234_lessons.py first!")
        return
    
    # Characters
    characters_data = [
        {"character": "点", "pinyin": "diǎn", "meaning": "o'clock", "hsk_level": 2, "stroke_count": 9},
        {"character": "分", "pinyin": "fēn", "meaning": "minute", "hsk_level": 2, "stroke_count": 4},
        {"character": "半", "pinyin": "bàn", "meaning": "half", "hsk_level": 2, "stroke_count": 5},
        {"character": "刻", "pinyin": "kè", "meaning": "quarter (15 min)", "hsk_level": 2, "stroke_count": 8},
        {"character": "钟", "pinyin": "zhōng", "meaning": "clock", "hsk_level": 2, "stroke_count": 9},
        {"character": "天", "pinyin": "tiān", "meaning": "day", "hsk_level": 2, "stroke_count": 4},
        {"character": "年", "pinyin": "nián", "meaning": "year", "hsk_level": 2, "stroke_count": 6},
        {"character": "月", "pinyin": "yuè", "meaning": "month", "hsk_level": 2, "stroke_count": 4},
        {"character": "日", "pinyin": "rì", "meaning": "day/date", "hsk_level": 2, "stroke_count": 4},
        {"character": "号", "pinyin": "hào", "meaning": "date/number", "hsk_level": 2, "stroke_count": 5},
    ]
    add_characters_to_lesson(db, lesson, characters_data)
    
    # Vocabulary
    vocab_items = [
        {"word": "点钟", "pinyin": "diǎn zhōng", "meaning": "o'clock", "example": "现在三点钟。(xiàn zài sān diǎn zhōng) - It's 3 o'clock now.", "hsk_level": 2},
        {"word": "分钟", "pinyin": "fēn zhōng", "meaning": "minute", "example": "十分钟 (shí fēn zhōng) - 10 minutes", "hsk_level": 2},
        {"word": "半", "pinyin": "bàn", "meaning": "half", "example": "三点半 (sān diǎn bàn) - 3:30", "hsk_level": 2},
        {"word": "一刻", "pinyin": "yī kè", "meaning": "quarter (15 min)", "example": "差一刻四点 (chà yī kè sì diǎn) - quarter to 4", "hsk_level": 2},
        {"word": "星期", "pinyin": "xīng qī", "meaning": "week", "example": "星期一 (xīng qī yī) - Monday", "hsk_level": 2},
        {"word": "今天", "pinyin": "jīn tiān", "meaning": "today", "example": "今天星期几？(jīn tiān xīng qī jǐ?) - What day is today?", "hsk_level": 2},
        {"word": "明天", "pinyin": "míng tiān", "meaning": "tomorrow", "example": "明天见！(míng tiān jiàn!) - See you tomorrow!", "hsk_level": 2},
        {"word": "昨天", "pinyin": "zuó tiān", "meaning": "yesterday", "example": "昨天很冷。(zuó tiān hěn lěng) - It was cold yesterday.", "hsk_level": 2},
        {"word": "上午", "pinyin": "shàng wǔ", "meaning": "morning (AM)", "example": "上午十点 (shàng wǔ shí diǎn) - 10 AM", "hsk_level": 2},
        {"word": "下午", "pinyin": "xià wǔ", "meaning": "afternoon (PM)", "example": "下午两点 (xià wǔ liǎng diǎn) - 2 PM", "hsk_level": 2},
    ]
    add_vocabulary_to_lesson(db, lesson, vocab_items)
    
    # Objectives
    db.query(LessonObjective).filter(LessonObjective.lesson_id == lesson.id).delete()
    objectives = [
        "Học cách nói giờ bằng tiếng Trung",
        "Nắm vững từ vựng về ngày, tháng, năm",
        "Hỏi và trả lời về thời gian",
        "Sử dụng 点, 分, 半 để nói giờ chính xác",
    ]
    for idx, obj_text in enumerate(objectives):
        db.add(LessonObjective(lesson_id=lesson.id, objective=obj_text, order=idx))
    
    # Grammar
    db.query(GrammarExample).filter(
        GrammarExample.grammar_point_id.in_(
            db.query(GrammarPoint.id).filter(GrammarPoint.lesson_id == lesson.id)
        )
    ).delete(synchronize_session=False)
    db.query(GrammarPoint).filter(GrammarPoint.lesson_id == lesson.id).delete()
    
    grammar1 = GrammarPoint(
        lesson_id=lesson.id,
        title="Nói giờ - 几点？(jǐ diǎn?)",
        explanation="Dùng 点(diǎn) cho giờ và 分(fēn) cho phút. Cấu trúc: X点Y分",
        order=1
    )
    db.add(grammar1)
    db.flush()
    
    examples = [
        {"grammar_point_id": grammar1.id, "example": "三点 (sān diǎn)", "translation": "3 giờ", "order": 1},
        {"grammar_point_id": grammar1.id, "example": "五点十分 (wǔ diǎn shí fēn)", "translation": "5:10", "order": 2},
        {"grammar_point_id": grammar1.id, "example": "七点半 (qī diǎn bàn)", "translation": "7:30", "order": 3},
    ]
    for ex in examples:
        db.add(GrammarExample(**ex))
    
    # Exercises
    db.query(Exercise).filter(Exercise.lesson_id == lesson.id).delete()
    exercises = [
        {"lesson_id": lesson.id, "type": "multiple_choice", "question": "'Bây giờ mấy giờ?' trong tiếng Trung là gì?", "answer": "现在几点？", "options": '["现在几点？", "今天星期几？", "你好吗？", "多少钱？"]', "order": 1},
        {"lesson_id": lesson.id, "type": "translation", "question": "Dịch: '3:30'", "answer": "三点半", "options": '[]', "order": 2},
        {"lesson_id": lesson.id, "type": "fill_blank", "question": "Điền: 现在五___十分 (Bây giờ 5:10)", "answer": "点", "options": '["点", "分", "半", "刻"]', "order": 3},
    ]
    for ex in exercises:
        db.add(Exercise(**ex))
    
    db.commit()
    print("   [SUCCESS] Time and Date lesson completed")

def seed_weather_and_seasons(db):
    """Seed Weather and Seasons lesson (HSK 2 - Lesson 2)"""
    print("\n[HSK 2.2] Seeding Weather and Seasons...")
    
    lesson = db.query(Lesson).filter(Lesson.title == "Weather and Seasons", Lesson.hsk_level == 2).first()
    if not lesson:
        return
    
    characters_data = [
        {"character": "天", "pinyin": "tiān", "meaning": "sky/day", "hsk_level": 2, "stroke_count": 4},
        {"character": "气", "pinyin": "qì", "meaning": "air/gas", "hsk_level": 2, "stroke_count": 4},
        {"character": "冷", "pinyin": "lěng", "meaning": "cold", "hsk_level": 2, "stroke_count": 7},
        {"character": "热", "pinyin": "rè", "meaning": "hot", "hsk_level": 2, "stroke_count": 10},
        {"character": "雨", "pinyin": "yǔ", "meaning": "rain", "hsk_level": 2, "stroke_count": 8},
        {"character": "雪", "pinyin": "xuě", "meaning": "snow", "hsk_level": 2, "stroke_count": 11},
        {"character": "风", "pinyin": "fēng", "meaning": "wind", "hsk_level": 2, "stroke_count": 4},
        {"character": "春", "pinyin": "chūn", "meaning": "spring", "hsk_level": 2, "stroke_count": 9},
        {"character": "夏", "pinyin": "xià", "meaning": "summer", "hsk_level": 2, "stroke_count": 10},
        {"character": "秋", "pinyin": "qiū", "meaning": "autumn", "hsk_level": 2, "stroke_count": 9},
        {"character": "冬", "pinyin": "dōng", "meaning": "winter", "hsk_level": 2, "stroke_count": 5},
    ]
    add_characters_to_lesson(db, lesson, characters_data)
    
    vocab_items = [
        {"word": "天气", "pinyin": "tiān qì", "meaning": "weather", "example": "今天天气很好。(jīn tiān tiān qì hěn hǎo) - The weather is nice today.", "hsk_level": 2},
        {"word": "下雨", "pinyin": "xià yǔ", "meaning": "to rain", "example": "明天会下雨。(míng tiān huì xià yǔ) - It will rain tomorrow.", "hsk_level": 2},
        {"word": "下雪", "pinyin": "xià xuě", "meaning": "to snow", "example": "冬天常下雪。(dōng tiān cháng xià xuě) - It often snows in winter.", "hsk_level": 2},
        {"word": "刮风", "pinyin": "guā fēng", "meaning": "to be windy", "example": "今天刮风。(jīn tiān guā fēng) - It's windy today.", "hsk_level": 2},
        {"word": "春天", "pinyin": "chūn tiān", "meaning": "spring", "example": "春天很美。(chūn tiān hěn měi) - Spring is beautiful.", "hsk_level": 2},
        {"word": "夏天", "pinyin": "xià tiān", "meaning": "summer", "example": "夏天很热。(xià tiān hěn rè) - Summer is hot.", "hsk_level": 2},
        {"word": "秋天", "pinyin": "qiū tiān", "meaning": "autumn", "example": "秋天很凉快。(qiū tiān hěn liáng kuai) - Autumn is cool.", "hsk_level": 2},
        {"word": "冬天", "pinyin": "dōng tiān", "meaning": "winter", "example": "冬天很冷。(dōng tiān hěn lěng) - Winter is cold.", "hsk_level": 2},
    ]
    add_vocabulary_to_lesson(db, lesson, vocab_items)
    
    db.query(LessonObjective).filter(LessonObjective.lesson_id == lesson.id).delete()
    objectives = [
        "Học từ vựng về thời tiết",
        "Mô tả các mùa trong năm",
        "Hỏi và trả lời về thời tiết",
    ]
    for idx, obj_text in enumerate(objectives):
        db.add(LessonObjective(lesson_id=lesson.id, objective=obj_text, order=idx))
    
    db.query(GrammarExample).filter(
        GrammarExample.grammar_point_id.in_(
            db.query(GrammarPoint.id).filter(GrammarPoint.lesson_id == lesson.id)
        )
    ).delete(synchronize_session=False)
    db.query(GrammarPoint).filter(GrammarPoint.lesson_id == lesson.id).delete()
    
    grammar1 = GrammarPoint(
        lesson_id=lesson.id,
        title="Mô tả thời tiết",
        explanation="Dùng 下 (xià) + thời tiết. VD: 下雨 (mưa), 下雪 (tuyết)",
        order=1
    )
    db.add(grammar1)
    db.flush()
    db.add(GrammarExample(grammar_point_id=grammar1.id, example="今天下雨。(jīn tiān xià yǔ)", translation="Hôm nay mưa.", order=1))
    
    db.query(Exercise).filter(Exercise.lesson_id == lesson.id).delete()
    exercises = [
        {"lesson_id": lesson.id, "type": "multiple_choice", "question": "'Mùa xuân' trong tiếng Trung là gì?", "answer": "春天", "options": '["春天", "夏天", "秋天", "冬天"]', "order": 1},
        {"lesson_id": lesson.id, "type": "translation", "question": "Dịch: 'Hôm nay trời nóng'", "answer": "今天很热", "options": '[]', "order": 2},
    ]
    for ex in exercises:
        db.add(Exercise(**ex))
    
    db.commit()
    print("   [SUCCESS] Weather and Seasons lesson completed")

def seed_all_hsk2_lessons():
    """Seed all HSK 2 lessons with details"""
    db = SessionLocal()
    
    try:
        print("=" * 80)
        print("Seeding All HSK 2 Lesson Details...")
        print("=" * 80)
        
        seed_time_and_date(db)
        seed_weather_and_seasons(db)
        
        print("\n" + "=" * 80)
        print("[SUCCESS] All HSK 2 lessons seeded!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_all_hsk2_lessons()