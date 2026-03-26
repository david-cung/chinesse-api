import sys
import os
sys.path.append('.')

from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.lesson import Lesson, Vocabulary, LessonObjective, GrammarPoint, GrammarExample, Exercise
from models.character import Character
from models.sentence import Sentence

def fix_hsk1_lessons():
    db = SessionLocal()
    try:
        print("🚀 Starting HSK 1 Lesson Data Fix...")
        
        # 1. Update existing HSK 1 lessons (Bài 5 - Bài 14)
        # These currently have orders 1-10. We need to shift them to 5-14.
        existing_lessons = db.query(Lesson).filter(Lesson.hsk_level == 1).order_by(Lesson.order.desc()).all()
        for lesson in existing_lessons:
            if "Bài 5" in lesson.title or "Bài 6" in lesson.title or "Bài 7" in lesson.title or \
               "Bài 8" in lesson.title or "Bài 9" in lesson.title or "Bài 10" in lesson.title or \
               "Bài 11" in lesson.title or "Bài 12" in lesson.title or "Bài 13" in lesson.title or \
               "Bài 14" in lesson.title:
                
                # Check if it's already shifted (idempotency)
                if lesson.order <= 10:
                    old_order = lesson.order
                    lesson.order = old_order + 4
                    print(f"   ⬆️  Shifted '{lesson.title}': {old_order} -> {lesson.order}")

        db.flush()

        # 2. Add/Verify Lesson 1-4
        lessons_to_add = [
            {
                "order": 1,
                "title": "Bài 1: Chào hỏi cơ bản",
                "description": "Học các câu chào hỏi và làm quen cơ bản",
                "estimated_time": 25,
                "vocab": [
                    {"word": "你好", "pinyin": "nǐ hǎo", "meaning": "xin chào"},
                    {"word": "您好", "pinyin": "nín hǎo", "meaning": "chào ngài (kính trọng)"},
                    {"word": "早上好", "pinyin": "zǎo shang hǎo", "meaning": "chào buổi sáng"},
                    {"word": "老师好", "pinyin": "lǎo shī hǎo", "meaning": "chào thầy/cô"},
                    {"word": "再见", "pinyin": "zài jiàn", "meaning": "tạm biệt"},
                    {"word": "谢谢", "pinyin": "xiè xie", "meaning": "cảm ơn"},
                    {"word": "不客气", "pinyin": "bù kè qì", "meaning": "đừng khách khí"},
                    {"word": "对不起", "pinyin": "duì bù qǐ", "meaning": "xin lỗi"},
                    {"word": "没关系", "pinyin": "méi guān xì", "meaning": "không có gì"},
                ]
            },
            {
                "order": 2,
                "title": "Bài 2: Tự giới thiệu",
                "description": "Học cách giới thiệu tên, tuổi và quốc tịch",
                "estimated_time": 30,
                "vocab": [
                    {"word": "我", "pinyin": "wǒ", "meaning": "tôi, mình"},
                    {"word": "你", "pinyin": "nǐ", "meaning": "bạn, cậu"},
                    {"word": "叫", "pinyin": "jiào", "meaning": "tên là, gọi là"},
                    {"word": "什么", "pinyin": "shén me", "meaning": "cái gì"},
                    {"word": "名字", "pinyin": "míng zi", "meaning": "tên"},
                    {"word": "是", "pinyin": "shì", "meaning": "là"},
                    {"word": "老师", "pinyin": "lǎo shī", "meaning": "giáo viên"},
                    {"word": "学生", "pinyin": "xué sheng", "meaning": "học sinh, sinh viên"},
                    {"word": "人", "pinyin": "rén", "meaning": "người"},
                    {"word": "越南", "pinyin": "Yuè nán", "meaning": "Việt Nam"},
                    {"word": "中国", "pinyin": "Zhōng guó", "meaning": "Trung Quốc"},
                ]
            },
            {
                "order": 3,
                "title": "Bài 3: Số đếm",
                "description": "Cách đếm số từ 1 đến 100",
                "estimated_time": 30,
                "vocab": [
                    {"word": "一", "pinyin": "yī", "meaning": "số 1"},
                    {"word": "二", "pinyin": "èr", "meaning": "số 2"},
                    {"word": "三", "pinyin": "sān", "meaning": "số 3"},
                    {"word": "四", "pinyin": "sì", "meaning": "số 4"},
                    {"word": "五", "pinyin": "wǔ", "meaning": "số 5"},
                    {"word": "六", "pinyin": "liù", "meaning": "số 6"},
                    {"word": "七", "pinyin": "qī", "meaning": "số 7"},
                    {"word": "八", "pinyin": "bā", "meaning": "số 8"},
                    {"word": "九", "pinyin": "jiǔ", "meaning": "số 9"},
                    {"word": "十", "pinyin": "shí", "meaning": "số 10"},
                    {"word": "百", "pinyin": "bǎi", "meaning": "trăm"},
                    {"word": "几", "pinyin": "jǐ", "meaning": "mấy"},
                    {"word": "多少", "pinyin": "duō shao", "meaning": "bao nhiêu"},
                ]
            },
            {
                "order": 4,
                "title": "Bài 4: Gia đình",
                "description": "Các thành viên trong gia đình",
                "estimated_time": 30,
                "vocab": [
                    {"word": "家", "pinyin": "jiā", "meaning": "gia đình, nhà"},
                    {"word": "爸爸", "pinyin": "bà ba", "meaning": "bố"},
                    {"word": "妈妈", "pinyin": "mā ma", "meaning": "mẹ"},
                    {"word": "哥哥", "pinyin": "gē ge", "meaning": "anh trai"},
                    {"word": "弟弟", "pinyin": "dì di", "meaning": "em trai"},
                    {"word": "姐姐", "pinyin": "jiě jie", "meaning": "chị gái"},
                    {"word": "妹妹", "pinyin": "mèi mei", "meaning": "em gái"},
                    {"word": "有", "pinyin": "yǒu", "meaning": "có"},
                    {"word": "没有", "pinyin": "méi yǒu", "meaning": "không có"},
                ]
            }
        ]

        for ld in lessons_to_add:
            # Check if exists
            exists = db.query(Lesson).filter(Lesson.hsk_level == 1, Lesson.order == ld["order"]).first()
            if exists:
                print(f"   ⏩  Lesson {ld['order']} already exists: {exists.title}. Updating info...")
                exists.title = ld["title"]
                exists.description = ld["description"]
                lesson = exists
            else:
                lesson = Lesson(
                    title=ld["title"],
                    description=ld["description"],
                    hsk_level=1,
                    order=ld["order"],
                    estimated_time=ld["estimated_time"],
                    is_published=True
                )
                db.add(lesson)
                db.flush()
                print(f"   ✅ Created '{ld['title']}'")

            # Add vocab if empty
            if len(lesson.vocabularies) == 0:
                for v_data in ld["vocab"]:
                    vocab = db.query(Vocabulary).filter(Vocabulary.word == v_data["word"]).first()
                    if not vocab:
                        vocab = Vocabulary(
                            word=v_data["word"],
                            pinyin=v_data["pinyin"],
                            meaning=v_data["meaning"],
                            hsk_level=1
                        )
                        db.add(vocab)
                        db.flush()
                    lesson.vocabularies.append(vocab)
                print(f"      Mapped {len(ld['vocab'])} vocab items")

        db.commit()
        print("\n✨ HSK 1 Lesson Data Fix Completed!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error during fix: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    fix_hsk1_lessons()
