"""
Seed script for 10 new HSK1 lessons
Topics with gradually increasing difficulty for beginners
"""
from database.database import SessionLocal
from models.user import User
from models.character import Character
from models.progress import DailyMission
from models.review import ReviewCard, ReviewRating, ReviewSession
from models.quiz import QuizAttempt, WordStats
from models.sentence import Sentence
from models.lesson import Lesson, Vocabulary, LessonObjective, Exercise

def seed_hsk1_lessons():
    db = SessionLocal()
    
    try:
        # Check current max order
        max_order = db.query(Lesson).filter(Lesson.hsk_level == 1).count()
        
        lessons_data = [
            # Lesson 5: Colors - Very basic, visual learning
            {
                "title": "Bài 5: Màu sắc",
                "description": "Học các màu sắc cơ bản trong tiếng Trung",
                "order": max_order + 1,
                "estimated_time": 8,
                "vocabularies": [
                    {"word": "红", "pinyin": "hóng", "meaning": "màu đỏ"},
                    {"word": "蓝", "pinyin": "lán", "meaning": "màu xanh dương"},
                    {"word": "绿", "pinyin": "lǜ", "meaning": "màu xanh lá"},
                    {"word": "黄", "pinyin": "huáng", "meaning": "màu vàng"},
                    {"word": "白", "pinyin": "bái", "meaning": "màu trắng"},
                    {"word": "黑", "pinyin": "hēi", "meaning": "màu đen"},
                    {"word": "颜色", "pinyin": "yánsè", "meaning": "màu sắc"},
                ],
                "objectives": [
                    "Nhận biết 6 màu sắc cơ bản",
                    "Hỏi và trả lời về màu sắc",
                ],
            },
            # Lesson 6: Food & Drinks - Daily life
            {
                "title": "Bài 6: Đồ ăn thức uống",
                "description": "Học từ vựng về đồ ăn và thức uống hàng ngày",
                "order": max_order + 2,
                "estimated_time": 10,
                "vocabularies": [
                    {"word": "水", "pinyin": "shuǐ", "meaning": "nước"},
                    {"word": "茶", "pinyin": "chá", "meaning": "trà"},
                    {"word": "米饭", "pinyin": "mǐfàn", "meaning": "cơm"},
                    {"word": "面", "pinyin": "miàn", "meaning": "mì"},
                    {"word": "菜", "pinyin": "cài", "meaning": "rau, món ăn"},
                    {"word": "肉", "pinyin": "ròu", "meaning": "thịt"},
                    {"word": "水果", "pinyin": "shuǐguǒ", "meaning": "trái cây"},
                    {"word": "苹果", "pinyin": "píngguǒ", "meaning": "táo"},
                    {"word": "好吃", "pinyin": "hǎochī", "meaning": "ngon"},
                ],
                "objectives": [
                    "Gọi tên các loại đồ ăn thức uống",
                    "Diễn đạt sở thích ăn uống cơ bản",
                ],
            },
            # Lesson 7: Time expressions - Basic
            {
                "title": "Bài 7: Thời gian",
                "description": "Học cách nói giờ và các thời điểm trong ngày",
                "order": max_order + 3,
                "estimated_time": 12,
                "vocabularies": [
                    {"word": "今天", "pinyin": "jīntiān", "meaning": "hôm nay"},
                    {"word": "明天", "pinyin": "míngtiān", "meaning": "ngày mai"},
                    {"word": "昨天", "pinyin": "zuótiān", "meaning": "hôm qua"},
                    {"word": "早上", "pinyin": "zǎoshang", "meaning": "buổi sáng"},
                    {"word": "中午", "pinyin": "zhōngwǔ", "meaning": "buổi trưa"},
                    {"word": "晚上", "pinyin": "wǎnshang", "meaning": "buổi tối"},
                    {"word": "点", "pinyin": "diǎn", "meaning": "giờ (đồng hồ)"},
                    {"word": "分", "pinyin": "fēn", "meaning": "phút"},
                    {"word": "现在", "pinyin": "xiànzài", "meaning": "bây giờ"},
                ],
                "objectives": [
                    "Nói được giờ cơ bản",
                    "Phân biệt các thời điểm trong ngày",
                ],
            },
            # Lesson 8: Days & Months
            {
                "title": "Bài 8: Ngày tháng",
                "description": "Học các ngày trong tuần và tháng trong năm",
                "order": max_order + 4,
                "estimated_time": 10,
                "vocabularies": [
                    {"word": "星期", "pinyin": "xīngqī", "meaning": "tuần"},
                    {"word": "星期一", "pinyin": "xīngqī yī", "meaning": "thứ hai"},
                    {"word": "星期天", "pinyin": "xīngqī tiān", "meaning": "chủ nhật"},
                    {"word": "月", "pinyin": "yuè", "meaning": "tháng"},
                    {"word": "年", "pinyin": "nián", "meaning": "năm"},
                    {"word": "号", "pinyin": "hào", "meaning": "ngày (trong tháng)"},
                    {"word": "生日", "pinyin": "shēngrì", "meaning": "sinh nhật"},
                ],
                "objectives": [
                    "Nói được các ngày trong tuần",
                    "Diễn đạt ngày tháng năm",
                ],
            },
            # Lesson 9: Weather
            {
                "title": "Bài 9: Thời tiết",
                "description": "Mô tả thời tiết và nhiệt độ",
                "order": max_order + 5,
                "estimated_time": 10,
                "vocabularies": [
                    {"word": "天气", "pinyin": "tiānqì", "meaning": "thời tiết"},
                    {"word": "热", "pinyin": "rè", "meaning": "nóng"},
                    {"word": "冷", "pinyin": "lěng", "meaning": "lạnh"},
                    {"word": "下雨", "pinyin": "xià yǔ", "meaning": "mưa"},
                    {"word": "晴天", "pinyin": "qíngtiān", "meaning": "trời nắng"},
                    {"word": "风", "pinyin": "fēng", "meaning": "gió"},
                    {"word": "太阳", "pinyin": "tàiyáng", "meaning": "mặt trời"},
                ],
                "objectives": [
                    "Mô tả thời tiết hôm nay",
                    "Hỏi về thời tiết",
                ],
            },
            # Lesson 10: Location & Places
            {
                "title": "Bài 10: Địa điểm",
                "description": "Học các địa điểm phổ biến và cách chỉ đường cơ bản",
                "order": max_order + 6,
                "estimated_time": 12,
                "vocabularies": [
                    {"word": "这里", "pinyin": "zhèlǐ", "meaning": "ở đây"},
                    {"word": "那里", "pinyin": "nàlǐ", "meaning": "ở kia"},
                    {"word": "哪里", "pinyin": "nǎlǐ", "meaning": "ở đâu"},
                    {"word": "学校", "pinyin": "xuéxiào", "meaning": "trường học"},
                    {"word": "医院", "pinyin": "yīyuàn", "meaning": "bệnh viện"},
                    {"word": "商店", "pinyin": "shāngdiàn", "meaning": "cửa hàng"},
                    {"word": "饭店", "pinyin": "fàndiàn", "meaning": "nhà hàng"},
                    {"word": "家", "pinyin": "jiā", "meaning": "nhà"},
                ],
                "objectives": [
                    "Hỏi và chỉ vị trí",
                    "Gọi tên các địa điểm công cộng",
                ],
            },
            # Lesson 11: Transportation
            {
                "title": "Bài 11: Phương tiện giao thông",
                "description": "Từ vựng về các phương tiện di chuyển",
                "order": max_order + 7,
                "estimated_time": 10,
                "vocabularies": [
                    {"word": "车", "pinyin": "chē", "meaning": "xe"},
                    {"word": "汽车", "pinyin": "qìchē", "meaning": "ô tô"},
                    {"word": "公共汽车", "pinyin": "gōnggòng qìchē", "meaning": "xe buýt"},
                    {"word": "出租车", "pinyin": "chūzū chē", "meaning": "taxi"},
                    {"word": "飞机", "pinyin": "fēijī", "meaning": "máy bay"},
                    {"word": "火车", "pinyin": "huǒchē", "meaning": "tàu hỏa"},
                    {"word": "走", "pinyin": "zǒu", "meaning": "đi bộ"},
                ],
                "objectives": [
                    "Gọi tên các phương tiện giao thông",
                    "Nói cách di chuyển đến một nơi",
                ],
            },
            # Lesson 12: Shopping basics
            {
                "title": "Bài 12: Mua sắm cơ bản",
                "description": "Học cách hỏi giá và mua đồ",
                "order": max_order + 8,
                "estimated_time": 12,
                "vocabularies": [
                    {"word": "买", "pinyin": "mǎi", "meaning": "mua"},
                    {"word": "卖", "pinyin": "mài", "meaning": "bán"},
                    {"word": "钱", "pinyin": "qián", "meaning": "tiền"},
                    {"word": "块", "pinyin": "kuài", "meaning": "đồng (tiền)"},
                    {"word": "多少", "pinyin": "duōshao", "meaning": "bao nhiêu"},
                    {"word": "贵", "pinyin": "guì", "meaning": "đắt"},
                    {"word": "便宜", "pinyin": "piányi", "meaning": "rẻ"},
                    {"word": "要", "pinyin": "yào", "meaning": "muốn, cần"},
                ],
                "objectives": [
                    "Hỏi giá cả của đồ vật",
                    "Thực hiện giao dịch mua bán đơn giản",
                ],
            },
            # Lesson 13: Daily activities
            {
                "title": "Bài 13: Hoạt động hàng ngày",
                "description": "Mô tả các hoạt động thường ngày",
                "order": max_order + 9,
                "estimated_time": 12,
                "vocabularies": [
                    {"word": "起床", "pinyin": "qǐchuáng", "meaning": "thức dậy"},
                    {"word": "睡觉", "pinyin": "shuìjiào", "meaning": "ngủ"},
                    {"word": "吃饭", "pinyin": "chīfàn", "meaning": "ăn cơm"},
                    {"word": "喝水", "pinyin": "hē shuǐ", "meaning": "uống nước"},
                    {"word": "工作", "pinyin": "gōngzuò", "meaning": "làm việc"},
                    {"word": "学习", "pinyin": "xuéxí", "meaning": "học tập"},
                    {"word": "看书", "pinyin": "kàn shū", "meaning": "đọc sách"},
                    {"word": "看电视", "pinyin": "kàn diànshì", "meaning": "xem TV"},
                ],
                "objectives": [
                    "Mô tả lịch trình hàng ngày",
                    "Kể về các hoạt động thường làm",
                ],
            },
            # Lesson 14: Feelings & Emotions
            {
                "title": "Bài 14: Cảm xúc",
                "description": "Diễn đạt cảm xúc và trạng thái",
                "order": max_order + 10,
                "estimated_time": 10,
                "vocabularies": [
                    {"word": "高兴", "pinyin": "gāoxìng", "meaning": "vui vẻ"},
                    {"word": "难过", "pinyin": "nánguò", "meaning": "buồn"},
                    {"word": "累", "pinyin": "lèi", "meaning": "mệt"},
                    {"word": "饿", "pinyin": "è", "meaning": "đói"},
                    {"word": "渴", "pinyin": "kě", "meaning": "khát"},
                    {"word": "忙", "pinyin": "máng", "meaning": "bận"},
                    {"word": "喜欢", "pinyin": "xǐhuan", "meaning": "thích"},
                    {"word": "爱", "pinyin": "ài", "meaning": "yêu"},
                ],
                "objectives": [
                    "Diễn đạt cảm xúc của bản thân",
                    "Hỏi thăm cảm xúc người khác",
                ],
            },
        ]
        
        created_count = 0
        
        for lesson_data in lessons_data:
            # Check if lesson already exists
            exists = db.query(Lesson).filter(
                Lesson.title == lesson_data["title"],
                Lesson.hsk_level == 1
            ).first()
            
            if exists:
                print(f"⏭️  Skipping: {lesson_data['title']} (already exists)")
                continue
            
            # Create lesson
            lesson = Lesson(
                title=lesson_data["title"],
                description=lesson_data["description"],
                hsk_level=1,
                order=lesson_data["order"],
                estimated_time=lesson_data["estimated_time"],
                is_published=True
            )
            db.add(lesson)
            db.flush()  # Get lesson ID
            
            # Add vocabularies
            for vocab_data in lesson_data.get("vocabularies", []):
                # Check if vocabulary exists
                vocab = db.query(Vocabulary).filter(
                    Vocabulary.word == vocab_data["word"]
                ).first()
                
                if not vocab:
                    vocab = Vocabulary(
                        word=vocab_data["word"],
                        pinyin=vocab_data["pinyin"],
                        meaning=vocab_data["meaning"],
                        hsk_level=1
                    )
                    db.add(vocab)
                    db.flush()
                
                # Link to lesson
                lesson.vocabularies.append(vocab)
            
            # Add objectives
            for i, obj_text in enumerate(lesson_data.get("objectives", [])):
                obj = LessonObjective(
                    lesson_id=lesson.id,
                    objective=obj_text,
                    order=i + 1
                )
                db.add(obj)
            
            print(f"✅ Created: {lesson_data['title']} ({len(lesson_data.get('vocabularies', []))} words)")
            created_count += 1
        
        db.commit()
        print(f"\n🎉 Done! Created {created_count} new lessons")
        
        # Show final count
        total = db.query(Lesson).filter(Lesson.hsk_level == 1).count()
        print(f"📚 Total HSK1 lessons: {total}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_hsk1_lessons()
