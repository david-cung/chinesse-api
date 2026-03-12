# seed_family_members.py
import sys
sys.path.append('.')

from sqlalchemy.orm import Session
from database.database import SessionLocal, engine
from models.user import User
from models.character import Character
from models.progress import DailyMission
from models.review import ReviewCard, ReviewRating, ReviewSession
from models.quiz import QuizAttempt, WordStats
from models.sentence import Sentence
from models.lesson import (
    Lesson, 
    Vocabulary, 
    LessonObjective, 
    GrammarPoint, 
    GrammarExample, 
    Exercise
)

def seed_family_members():
    """Seed detailed data for Family Members lesson (Lesson 4)"""
    db = SessionLocal()

    try:
        print("=" * 80)
        print("Seeding Family Members Lesson Details...")
        print("=" * 80)

        # Find or create Lesson 4
        lesson4 = db.query(Lesson).filter(Lesson.order == 4).first()
        
        if not lesson4:
            print("[INFO] Creating Family Members lesson...")
            lesson4 = Lesson(
                title="Family Members",
                description="Vocabulary for family relationships",
                hsk_level=1,
                order=4,
                estimated_time=30,
                is_published=True
            )
            db.add(lesson4)
            db.flush()
        else:
            print(f"[INFO] Found existing lesson: {lesson4.title}")

        # 1. Add/Link Characters
        print("\n[1/5] Adding characters...")
        characters_data = [
            {"character": "家", "pinyin": "jiā", "meaning": "family/home", "hsk_level": 1, "stroke_count": 10},
            {"character": "爸", "pinyin": "bà", "meaning": "dad", "hsk_level": 1, "stroke_count": 8},
            {"character": "妈", "pinyin": "mā", "meaning": "mom", "hsk_level": 1, "stroke_count": 6},
            {"character": "哥", "pinyin": "gē", "meaning": "older brother", "hsk_level": 1, "stroke_count": 10},
            {"character": "弟", "pinyin": "dì", "meaning": "younger brother", "hsk_level": 1, "stroke_count": 7},
            {"character": "姐", "pinyin": "jiě", "meaning": "older sister", "hsk_level": 1, "stroke_count": 8},
            {"character": "妹", "pinyin": "mèi", "meaning": "younger sister", "hsk_level": 1, "stroke_count": 8},
            {"character": "儿", "pinyin": "ér", "meaning": "son/child", "hsk_level": 1, "stroke_count": 2},
            {"character": "女", "pinyin": "nǚ", "meaning": "daughter/female", "hsk_level": 1, "stroke_count": 3},
            {"character": "人", "pinyin": "rén", "meaning": "person", "hsk_level": 1, "stroke_count": 2},
        ]

        lesson4.characters.clear()
        for char_data in characters_data:
            char = db.query(Character).filter(Character.character == char_data["character"]).first()
            if not char:
                char = Character(**char_data)
                db.add(char)
                db.flush()
            lesson4.characters.append(char)
        
        db.flush()
        print(f"   [SUCCESS] Linked {len(characters_data)} characters")

        # 2. Add Vocabulary
        print("\n[2/5] Adding vocabulary...")
        lesson4.vocabularies.clear()
        
        vocab_items = [
            {
                "word": "家", 
                "pinyin": "jiā", 
                "meaning": "family/home", 
                "example": "我家有四口人。(wǒ jiā yǒu sì kǒu rén) - My family has 4 people.",
                "hsk_level": 1
            },
            {
                "word": "爸爸", 
                "pinyin": "bà ba", 
                "meaning": "father/dad", 
                "example": "我爸爸是老师。(wǒ bà ba shì lǎo shī) - My dad is a teacher.",
                "hsk_level": 1
            },
            {
                "word": "妈妈", 
                "pinyin": "mā ma", 
                "meaning": "mother/mom", 
                "example": "妈妈很忙。(mā ma hěn máng) - Mom is very busy.",
                "hsk_level": 1
            },
            {
                "word": "哥哥", 
                "pinyin": "gē ge", 
                "meaning": "older brother", 
                "example": "我有一个哥哥。(wǒ yǒu yī gè gē ge) - I have one older brother.",
                "hsk_level": 1
            },
            {
                "word": "弟弟", 
                "pinyin": "dì di", 
                "meaning": "younger brother", 
                "example": "弟弟很可爱。(dì di hěn kě ài) - Younger brother is very cute.",
                "hsk_level": 1
            },
            {
                "word": "姐姐", 
                "pinyin": "jiě jie", 
                "meaning": "older sister", 
                "example": "姐姐在学校。(jiě jie zài xué xiào) - Older sister is at school.",
                "hsk_level": 1
            },
            {
                "word": "妹妹", 
                "pinyin": "mèi mei", 
                "meaning": "younger sister", 
                "example": "我的妹妹五岁。(wǒ de mèi mei wǔ suì) - My younger sister is 5 years old.",
                "hsk_level": 1
            },
            {
                "word": "儿子", 
                "pinyin": "ér zi", 
                "meaning": "son", 
                "example": "他有两个儿子。(tā yǒu liǎng gè ér zi) - He has two sons.",
                "hsk_level": 1
            },
            {
                "word": "女儿", 
                "pinyin": "nǚ ér", 
                "meaning": "daughter", 
                "example": "她的女儿很聪明。(tā de nǚ ér hěn cōng míng) - Her daughter is very smart.",
                "hsk_level": 1
            },
            {
                "word": "老公", 
                "pinyin": "lǎo gōng", 
                "meaning": "husband", 
                "example": "我老公很好。(wǒ lǎo gōng hěn hǎo) - My husband is very good.",
                "hsk_level": 1
            },
            {
                "word": "老婆", 
                "pinyin": "lǎo pó", 
                "meaning": "wife", 
                "example": "他老婆是医生。(tā lǎo pó shì yī shēng) - His wife is a doctor.",
                "hsk_level": 1
            },
            {
                "word": "孩子", 
                "pinyin": "hái zi", 
                "meaning": "child/children", 
                "example": "他们有三个孩子。(tā men yǒu sān gè hái zi) - They have three children.",
                "hsk_level": 1
            },
        ]

        for vocab_data in vocab_items:
            vocab = Vocabulary(**vocab_data)
            db.add(vocab)
            db.flush()
            lesson4.vocabularies.append(vocab)
        
        print(f"   [SUCCESS] Added {len(vocab_items)} vocabulary items")

        # 3. Add Objectives
        print("\n[3/5] Adding objectives...")
        db.query(LessonObjective).filter(LessonObjective.lesson_id == lesson4.id).delete()
        
        objectives = [
            "Học từ vựng về các thành viên trong gia đình",
            "Phân biệt anh/em trai, chị/em gái trong tiếng Trung",
            "Giới thiệu về gia đình của mình",
            "Hỏi về gia đình người khác",
            "Sử dụng '有' để nói về số lượng thành viên gia đình",
        ]
        
        for idx, obj_text in enumerate(objectives):
            obj = LessonObjective(
                lesson_id=lesson4.id, 
                objective=obj_text, 
                order=idx
            )
            db.add(obj)
        
        print(f"   [SUCCESS] Added {len(objectives)} objectives")

        # 4. Add Grammar Points
        print("\n[4/5] Adding grammar points...")
        
        db.query(GrammarExample).filter(
            GrammarExample.grammar_point_id.in_(
                db.query(GrammarPoint.id).filter(GrammarPoint.lesson_id == lesson4.id)
            )
        ).delete(synchronize_session=False)
        db.query(GrammarPoint).filter(GrammarPoint.lesson_id == lesson4.id).delete()
        
        # Grammar Point 1: Anh/Em trong tiếng Trung
        grammar1 = GrammarPoint(
            lesson_id=lesson4.id,
            title="Phân biệt Anh/Em - 哥哥/弟弟, 姐姐/妹妹",
            explanation="Tiếng Trung phân biệt rõ ràng người lớn tuổi hơn (哥/姐) và nhỏ tuổi hơn (弟/妹). 哥哥=anh trai, 弟弟=em trai, 姐姐=chị gái, 妹妹=em gái.",
            order=1
        )
        db.add(grammar1)
        db.flush()

        examples1 = [
            {
                "example": "我有一个哥哥。(wǒ yǒu yī gè gē ge)",
                "translation": "Tôi có một người anh trai (lớn hơn tôi).",
                "order": 1
            },
            {
                "example": "我有两个妹妹。(wǒ yǒu liǎng gè mèi mei)",
                "translation": "Tôi có hai em gái (nhỏ hơn tôi).",
                "order": 2
            },
            {
                "example": "你有弟弟吗？(nǐ yǒu dì di ma?)",
                "translation": "Bạn có em trai không?",
                "order": 3
            },
        ]

        for ex_data in examples1:
            ex = GrammarExample(grammar_point_id=grammar1.id, **ex_data)
            db.add(ex)

        # Grammar Point 2: Giới thiệu gia đình
        grammar2 = GrammarPoint(
            lesson_id=lesson4.id,
            title="我家有...口人 - Giới thiệu số người trong gia đình",
            explanation="Dùng '我家有...口人' để nói về số lượng thành viên gia đình. '口' là từ đo lường cho người trong gia đình.",
            order=2
        )
        db.add(grammar2)
        db.flush()

        examples2 = [
            {
                "example": "我家有四口人。(wǒ jiā yǒu sì kǒu rén)",
                "translation": "Gia đình tôi có 4 người.",
                "order": 1
            },
            {
                "example": "你家有几口人？(nǐ jiā yǒu jǐ kǒu rén?)",
                "translation": "Gia đình bạn có mấy người?",
                "order": 2
            },
            {
                "example": "他家有三口人：爸爸、妈妈和他。(tā jiā yǒu sān kǒu rén: bà ba, mā ma hé tā)",
                "translation": "Gia đình anh ấy có 3 người: bố, mẹ và anh ấy.",
                "order": 3
            },
        ]

        for ex_data in examples2:
            ex = GrammarExample(grammar_point_id=grammar2.id, **ex_data)
            db.add(ex)

        # Grammar Point 3: 的 - Sở hữu
        grammar3 = GrammarPoint(
            lesson_id=lesson4.id,
            title="的 (de) - Chỉ sở hữu",
            explanation="Dùng '的' giữa người sở hữu và đối tượng bị sở hữu. Cấu trúc: A + 的 + B = B của A.",
            order=3
        )
        db.add(grammar3)
        db.flush()

        examples3 = [
            {
                "example": "我的爸爸 (wǒ de bà ba)",
                "translation": "Bố của tôi",
                "order": 1
            },
            {
                "example": "他的妹妹 (tā de mèi mei)",
                "translation": "Em gái của anh ấy",
                "order": 2
            },
            {
                "example": "我们的家 (wǒ men de jiā)",
                "translation": "Gia đình của chúng tôi",
                "order": 3
            },
            {
                "example": "这是谁的儿子？(zhè shì shéi de ér zi?)",
                "translation": "Đây là con trai của ai?",
                "order": 4
            },
        ]

        for ex_data in examples3:
            ex = GrammarExample(grammar_point_id=grammar3.id, **ex_data)
            db.add(ex)

        print(f"   [SUCCESS] Added 3 grammar points with examples")

        # 5. Add Exercises
        print("\n[5/5] Adding exercises...")
        db.query(Exercise).filter(Exercise.lesson_id == lesson4.id).delete()
        
        exercises = [
            {
                "type": "multiple_choice",
                "question": "'Bố' trong tiếng Trung là gì?",
                "answer": "爸爸",
                "options": '["爸爸", "妈妈", "哥哥", "弟弟"]',
                "order": 1
            },
            {
                "type": "multiple_choice",
                "question": "Từ nào có nghĩa là 'em gái' (younger sister)?",
                "answer": "妹妹",
                "options": '["妹妹", "姐姐", "弟弟", "哥哥"]',
                "order": 2
            },
            {
                "type": "translation",
                "question": "Dịch sang tiếng Trung: 'Mẹ'",
                "answer": "妈妈",
                "options": '[]',
                "order": 3
            },
            {
                "type": "multiple_choice",
                "question": "'哥哥' có nghĩa là gì?",
                "answer": "anh trai",
                "options": '["anh trai", "em trai", "anh/chị", "em gái"]',
                "order": 4
            },
            {
                "type": "fill_blank",
                "question": "Điền từ: 我___有四口人。(Gia đình tôi có 4 người)",
                "answer": "家",
                "options": '["家", "爸", "妈", "人"]',
                "order": 5
            },
            {
                "type": "multiple_choice",
                "question": "Làm thế nào để nói 'con trai'?",
                "answer": "儿子",
                "options": '["儿子", "女儿", "孩子", "弟弟"]',
                "order": 6
            },
            {
                "type": "translation",
                "question": "Dịch: 'Gia đình bạn có mấy người?'",
                "answer": "你家有几口人？",
                "options": '[]',
                "order": 7
            },
            {
                "type": "fill_blank",
                "question": "Điền từ: 我___妹妹 (em gái của tôi)",
                "answer": "的",
                "options": '["的", "是", "有", "叫"]',
                "order": 8
            },
            {
                "type": "multiple_choice",
                "question": "'姐姐' và '妹妹' khác nhau như thế nào?",
                "answer": "姐姐 lớn tuổi hơn, 妹妹 nhỏ tuổi hơn",
                "options": '["姐姐 lớn tuổi hơn, 妹妹 nhỏ tuổi hơn", "姐姐 là con trai, 妹妹 là con gái", "Không khác nhau", "姐姐 là mẹ, 妹妹 là con"]',
                "order": 9
            },
            {
                "type": "multiple_choice",
                "question": "Từ đo lường cho người trong gia đình là gì?",
                "answer": "口",
                "options": '["口", "个", "位", "人"]',
                "order": 10
            },
        ]

        for ex_data in exercises:
            ex = Exercise(lesson_id=lesson4.id, **ex_data)
            db.add(ex)
        
        print(f"   [SUCCESS] Added {len(exercises)} exercises")

        # Commit all changes
        db.commit()

        # Verification
        print("\n" + "=" * 80)
        print("VERIFICATION - Family Members Lesson Details:")
        print("=" * 80)
        lesson_check = db.query(Lesson).filter(Lesson.id == lesson4.id).first()
        print(f"Title: {lesson_check.title}")
        print(f"  - Characters: {len(lesson_check.characters)}")
        print(f"  - Vocabulary: {len(lesson_check.vocabularies)}")
        print(f"  - Objectives: {len(lesson_check.objectives)}")
        print(f"  - Grammar Points: {len(lesson_check.grammar_points)}")
        print(f"  - Exercises: {len(lesson_check.exercises)}")

        print("\n" + "=" * 80)
        print("[SUCCESS] Family Members lesson seeded successfully!")
        print("=" * 80)
        print("\nTest API:")
        print(f"   curl http://localhost:8000/api/lessons/{lesson4.id}")
        print("=" * 80)

    except Exception as e:
        print(f"\n[ERROR] Error seeding Family Members: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()

    finally:
        db.close()

if __name__ == "__main__":
    seed_family_members()