# seed_hsk2_all_details.py
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

def clear_lesson_details(db, lesson):
    """Clear existing lesson details"""
    db.query(GrammarExample).filter(
        GrammarExample.grammar_point_id.in_(
            db.query(GrammarPoint.id).filter(GrammarPoint.lesson_id == lesson.id)
        )
    ).delete(synchronize_session=False)
    db.query(GrammarPoint).filter(GrammarPoint.lesson_id == lesson.id).delete()
    db.query(LessonObjective).filter(LessonObjective.lesson_id == lesson.id).delete()
    db.query(Exercise).filter(Exercise.lesson_id == lesson.id).delete()

# ============================================================================
# HSK 2.1 - TIME AND DATE
# ============================================================================
def seed_time_and_date(db):
    print("\n[HSK 2.1] Seeding Time and Date...")
    lesson = db.query(Lesson).filter(Lesson.title == "Time and Date", Lesson.hsk_level == 2).first()
    if not lesson:
        print("   [ERROR] Lesson not found!")
        return
    
    clear_lesson_details(db, lesson)
    
    characters_data = [
        {"character": "点", "pinyin": "diǎn", "meaning": "giờ", "hsk_level": 2, "stroke_count": 9},
        {"character": "分", "pinyin": "fēn", "meaning": "phút", "hsk_level": 2, "stroke_count": 4},
        {"character": "半", "pinyin": "bàn", "meaning": "nửa", "hsk_level": 2, "stroke_count": 5},
        {"character": "天", "pinyin": "tiān", "meaning": "ngày/trời", "hsk_level": 2, "stroke_count": 4},
        {"character": "年", "pinyin": "nián", "meaning": "năm", "hsk_level": 2, "stroke_count": 6},
        {"character": "月", "pinyin": "yuè", "meaning": "tháng", "hsk_level": 2, "stroke_count": 4},
        {"character": "日", "pinyin": "rì", "meaning": "ngày", "hsk_level": 2, "stroke_count": 4},
        {"character": "号", "pinyin": "hào", "meaning": "ngày (trong tháng)", "hsk_level": 2, "stroke_count": 5},
        {"character": "星", "pinyin": "xīng", "meaning": "ngôi sao", "hsk_level": 2, "stroke_count": 9},
        {"character": "期", "pinyin": "qī", "meaning": "kỳ hạn", "hsk_level": 2, "stroke_count": 12},
    ]
    add_characters_to_lesson(db, lesson, characters_data)
    
    vocab_items = [
        {"word": "点钟", "pinyin": "diǎn zhōng", "meaning": "giờ", "example": "现在三点钟。(xiàn zài sān diǎn zhōng) - Bây giờ 3 giờ.", "hsk_level": 2},
        {"word": "分钟", "pinyin": "fēn zhōng", "meaning": "phút", "example": "十分钟 (shí fēn zhōng) - 10 phút", "hsk_level": 2},
        {"word": "半", "pinyin": "bàn", "meaning": "rưỡi", "example": "三点半 (sān diǎn bàn) - 3 giờ rưỡi", "hsk_level": 2},
        {"word": "星期", "pinyin": "xīng qī", "meaning": "tuần", "example": "星期一 (xīng qī yī) - Thứ hai", "hsk_level": 2},
        {"word": "今天", "pinyin": "jīn tiān", "meaning": "hôm nay", "example": "今天星期几？(jīn tiān xīng qī jǐ?) - Hôm nay thứ mấy?", "hsk_level": 2},
        {"word": "明天", "pinyin": "míng tiān", "meaning": "ngày mai", "example": "明天见！(míng tiān jiàn!) - Hẹn gặp ngày mai!", "hsk_level": 2},
        {"word": "昨天", "pinyin": "zuó tiān", "meaning": "hôm qua", "example": "昨天很冷。(zuó tiān hěn lěng) - Hôm qua lạnh.", "hsk_level": 2},
        {"word": "上午", "pinyin": "shàng wǔ", "meaning": "buổi sáng", "example": "上午十点 (shàng wǔ shí diǎn) - 10 giờ sáng", "hsk_level": 2},
        {"word": "下午", "pinyin": "xià wǔ", "meaning": "buổi chiều", "example": "下午两点 (xià wǔ liǎng diǎn) - 2 giờ chiều", "hsk_level": 2},
        {"word": "现在", "pinyin": "xiàn zài", "meaning": "bây giờ", "example": "现在几点？(xiàn zài jǐ diǎn?) - Bây giờ mấy giờ?", "hsk_level": 2},
    ]
    add_vocabulary_to_lesson(db, lesson, vocab_items)
    
    for idx, obj in enumerate(["Học cách nói giờ bằng tiếng Trung", "Nắm vững từ vựng về ngày, tháng, năm", "Hỏi và trả lời về thời gian", "Sử dụng 点, 分, 半 để nói giờ chính xác"]):
        db.add(LessonObjective(lesson_id=lesson.id, objective=obj, order=idx))
    
    g1 = GrammarPoint(lesson_id=lesson.id, title="Nói giờ - X点Y分", explanation="Dùng 点 (diǎn) cho giờ và 分 (fēn) cho phút. Cấu trúc: số + 点 + số + 分. Ví dụ: 3:15 = 三点十五分", order=1)
    db.add(g1)
    db.flush()
    db.add(GrammarExample(grammar_point_id=g1.id, example="三点 (sān diǎn)", translation="3 giờ", order=1))
    db.add(GrammarExample(grammar_point_id=g1.id, example="五点半 (wǔ diǎn bàn)", translation="5 giờ rưỡi", order=2))
    db.add(GrammarExample(grammar_point_id=g1.id, example="七点十分 (qī diǎn shí fēn)", translation="7 giờ 10 phút", order=3))
    
    g2 = GrammarPoint(lesson_id=lesson.id, title="Nói ngày trong tuần - 星期", explanation="Dùng 星期 + số (1-6) cho thứ 2-7, 星期天 hoặc 星期日 cho Chủ nhật", order=2)
    db.add(g2)
    db.flush()
    db.add(GrammarExample(grammar_point_id=g2.id, example="今天星期三。(jīn tiān xīng qī sān)", translation="Hôm nay thứ tư", order=1))
    db.add(GrammarExample(grammar_point_id=g2.id, example="明天星期几？(míng tiān xīng qī jǐ?)", translation="Ngày mai thứ mấy?", order=2))
    
    for i, ex in enumerate([
        {"question": "'Bây giờ mấy giờ?' trong tiếng Trung là gì?", "answer": "现在几点？", "options": '["现在几点？", "今天星期几？", "你好吗？", "多少钱？"]'},
        {"question": "Dịch sang tiếng Trung: '3 giờ rưỡi'", "answer": "三点半", "options": '[]'},
        {"question": "Điền từ: 现在五___十分 (Bây giờ 5:10)", "answer": "点", "options": '["点", "分", "半", "刻"]'},
        {"question": "'Hôm nay' trong tiếng Trung là gì?", "answer": "今天", "options": '["今天", "明天", "昨天", "现在"]'},
        {"question": "Dịch: 'Thứ hai'", "answer": "星期一", "options": '[]'},
    ]):
        db.add(Exercise(lesson_id=lesson.id, type="multiple_choice", order=i+1, **ex))
    
    db.commit()
    print("   [SUCCESS]")

# ============================================================================
# HSK 2.2 - WEATHER AND SEASONS
# ============================================================================
def seed_weather_and_seasons(db):
    print("\n[HSK 2.2] Seeding Weather and Seasons...")
    lesson = db.query(Lesson).filter(Lesson.title == "Weather and Seasons", Lesson.hsk_level == 2).first()
    if not lesson:
        return
    
    clear_lesson_details(db, lesson)
    
    characters_data = [
        {"character": "天", "pinyin": "tiān", "meaning": "trời/ngày", "hsk_level": 2, "stroke_count": 4},
        {"character": "气", "pinyin": "qì", "meaning": "khí", "hsk_level": 2, "stroke_count": 4},
        {"character": "冷", "pinyin": "lěng", "meaning": "lạnh", "hsk_level": 2, "stroke_count": 7},
        {"character": "热", "pinyin": "rè", "meaning": "nóng", "hsk_level": 2, "stroke_count": 10},
        {"character": "雨", "pinyin": "yǔ", "meaning": "mưa", "hsk_level": 2, "stroke_count": 8},
        {"character": "雪", "pinyin": "xuě", "meaning": "tuyết", "hsk_level": 2, "stroke_count": 11},
        {"character": "风", "pinyin": "fēng", "meaning": "gió", "hsk_level": 2, "stroke_count": 4},
        {"character": "春", "pinyin": "chūn", "meaning": "xuân", "hsk_level": 2, "stroke_count": 9},
        {"character": "夏", "pinyin": "xià", "meaning": "hạ", "hsk_level": 2, "stroke_count": 10},
        {"character": "秋", "pinyin": "qiū", "meaning": "thu", "hsk_level": 2, "stroke_count": 9},
        {"character": "冬", "pinyin": "dōng", "meaning": "đông", "hsk_level": 2, "stroke_count": 5},
    ]
    add_characters_to_lesson(db, lesson, characters_data)
    
    vocab_items = [
        {"word": "天气", "pinyin": "tiān qì", "meaning": "thời tiết", "example": "今天天气很好。(jīn tiān tiān qì hěn hǎo) - Hôm nay thời tiết đẹp.", "hsk_level": 2},
        {"word": "下雨", "pinyin": "xià yǔ", "meaning": "mưa", "example": "明天会下雨。(míng tiān huì xià yǔ) - Ngày mai sẽ mưa.", "hsk_level": 2},
        {"word": "下雪", "pinyin": "xià xuě", "meaning": "tuyết rơi", "example": "冬天下雪。(dōng tiān xià xuě) - Mùa đông có tuyết.", "hsk_level": 2},
        {"word": "刮风", "pinyin": "guā fēng", "meaning": "gió thổi", "example": "今天刮风。(jīn tiān guā fēng) - Hôm nay có gió.", "hsk_level": 2},
        {"word": "春天", "pinyin": "chūn tiān", "meaning": "mùa xuân", "example": "春天很美。(chūn tiān hěn měi) - Mùa xuân đẹp.", "hsk_level": 2},
        {"word": "夏天", "pinyin": "xià tiān", "meaning": "mùa hè", "example": "夏天很热。(xià tiān hěn rè) - Mùa hè nóng.", "hsk_level": 2},
        {"word": "秋天", "pinyin": "qiū tiān", "meaning": "mùa thu", "example": "秋天凉快。(qiū tiān liáng kuai) - Mùa thu mát mẻ.", "hsk_level": 2},
        {"word": "冬天", "pinyin": "dōng tiān", "meaning": "mùa đông", "example": "冬天很冷。(dōng tiān hěn lěng) - Mùa đông lạnh.", "hsk_level": 2},
        {"word": "阴天", "pinyin": "yīn tiān", "meaning": "trời u ám", "example": "今天是阴天。(jīn tiān shì yīn tiān) - Hôm nay trời u ám.", "hsk_level": 2},
        {"word": "晴天", "pinyin": "qíng tiān", "meaning": "trời nắng", "example": "明天是晴天。(míng tiān shì qíng tiān) - Ngày mai trời nắng.", "hsk_level": 2},
    ]
    add_vocabulary_to_lesson(db, lesson, vocab_items)
    
    for idx, obj in enumerate(["Học từ vựng về thời tiết", "Mô tả các mùa trong năm", "Hỏi và trả lời về thời tiết", "Nói về sở thích theo mùa"]):
        db.add(LessonObjective(lesson_id=lesson.id, objective=obj, order=idx))
    
    g1 = GrammarPoint(lesson_id=lesson.id, title="下 + thời tiết", explanation="Dùng 下 (xià) với các hiện tượng thời tiết rơi xuống như mưa, tuyết. Ví dụ: 下雨 (mưa), 下雪 (tuyết rơi)", order=1)
    db.add(g1)
    db.flush()
    db.add(GrammarExample(grammar_point_id=g1.id, example="今天下雨。(jīn tiān xià yǔ)", translation="Hôm nay mưa.", order=1))
    db.add(GrammarExample(grammar_point_id=g1.id, example="北京常下雪。(běi jīng cháng xià xuě)", translation="Bắc Kinh thường có tuyết.", order=2))
    
    g2 = GrammarPoint(lesson_id=lesson.id, title="Hỏi thời tiết - 天气怎么样？", explanation="Dùng '天气怎么样？' để hỏi thời tiết như thế nào", order=2)
    db.add(g2)
    db.flush()
    db.add(GrammarExample(grammar_point_id=g2.id, example="今天天气怎么样？(jīn tiān tiān qì zěn me yàng?)", translation="Hôm nay thời tiết thế nào?", order=1))
    
    for i, ex in enumerate([
        {"question": "'Mùa xuân' trong tiếng Trung là gì?", "answer": "春天", "options": '["春天", "夏天", "秋天", "冬天"]'},
        {"question": "Dịch sang tiếng Trung: 'Hôm nay nóng'", "answer": "今天很热", "options": '[]'},
        {"question": "'下雨' có nghĩa là gì?", "answer": "mưa", "options": '["mưa", "tuyết", "gió", "nắng"]'},
        {"question": "Điền từ: 冬天很___ (Mùa đông lạnh)", "answer": "冷", "options": '["冷", "热", "好", "美"]'},
        {"question": "Dịch: 'Mùa thu mát mẻ'", "answer": "秋天凉快", "options": '[]'},
    ]):
        db.add(Exercise(lesson_id=lesson.id, type="multiple_choice", order=i+1, **ex))
    
    db.commit()
    print("   [SUCCESS]")

# ============================================================================
# HSK 2.3 - SHOPPING AND MONEY
# ============================================================================
def seed_shopping_and_money(db):
    print("\n[HSK 2.3] Seeding Shopping and Money...")
    lesson = db.query(Lesson).filter(Lesson.title == "Shopping and Money", Lesson.hsk_level == 2).first()
    if not lesson:
        return
    
    clear_lesson_details(db, lesson)
    
    characters_data = [
        {"character": "买", "pinyin": "mǎi", "meaning": "mua", "hsk_level": 2, "stroke_count": 6},
        {"character": "卖", "pinyin": "mài", "meaning": "bán", "hsk_level": 2, "stroke_count": 8},
        {"character": "钱", "pinyin": "qián", "meaning": "tiền", "hsk_level": 2, "stroke_count": 10},
        {"character": "块", "pinyin": "kuài", "meaning": "đồng (tiền)", "hsk_level": 2, "stroke_count": 7},
        {"character": "贵", "pinyin": "guì", "meaning": "đắt", "hsk_level": 2, "stroke_count": 9},
        {"character": "便", "pinyin": "pián", "meaning": "rẻ", "hsk_level": 2, "stroke_count": 9},
        {"character": "宜", "pinyin": "yí", "meaning": "thích hợp", "hsk_level": 2, "stroke_count": 8},
        {"character": "东", "pinyin": "dōng", "meaning": "đông/đồ", "hsk_level": 2, "stroke_count": 5},
        {"character": "西", "pinyin": "xī", "meaning": "tây/đồ", "hsk_level": 2, "stroke_count": 6},
        {"character": "商", "pinyin": "shāng", "meaning": "thương", "hsk_level": 2, "stroke_count": 11},
    ]
    add_characters_to_lesson(db, lesson, characters_data)
    
    vocab_items = [
        {"word": "买", "pinyin": "mǎi", "meaning": "mua", "example": "我想买这个。(wǒ xiǎng mǎi zhè ge) - Tôi muốn mua cái này.", "hsk_level": 2},
        {"word": "卖", "pinyin": "mài", "meaning": "bán", "example": "这里卖水果。(zhè lǐ mài shuǐ guǒ) - Ở đây bán trái cây.", "hsk_level": 2},
        {"word": "钱", "pinyin": "qián", "meaning": "tiền", "example": "多少钱？(duō shao qián?) - Bao nhiêu tiền?", "hsk_level": 2},
        {"word": "块", "pinyin": "kuài", "meaning": "đồng (đơn vị tiền tệ)", "example": "五块钱 (wǔ kuài qián) - 5 đồng", "hsk_level": 2},
        {"word": "贵", "pinyin": "guì", "meaning": "đắt", "example": "太贵了！(tài guì le!) - Đắt quá!", "hsk_level": 2},
        {"word": "便宜", "pinyin": "pián yi", "meaning": "rẻ", "example": "很便宜。(hěn pián yi) - Rất rẻ.", "hsk_level": 2},
        {"word": "东西", "pinyin": "dōng xi", "meaning": "đồ vật", "example": "买东西 (mǎi dōng xi) - mua đồ", "hsk_level": 2},
        {"word": "商店", "pinyin": "shāng diàn", "meaning": "cửa hàng", "example": "去商店 (qù shāng diàn) - đi cửa hàng", "hsk_level": 2},
        {"word": "市场", "pinyin": "shì chǎng", "meaning": "chợ", "example": "在市场 (zài shì chǎng) - ở chợ", "hsk_level": 2},
        {"word": "付钱", "pinyin": "fù qián", "meaning": "trả tiền", "example": "我来付钱。(wǒ lái fù qián) - Tôi trả tiền.", "hsk_level": 2},
    ]
    add_vocabulary_to_lesson(db, lesson, vocab_items)
    
    for idx, obj in enumerate(["Học từ vựng về mua sắm", "Hỏi giá cả", "Thương lượng giá", "Thanh toán"]):
        db.add(LessonObjective(lesson_id=lesson.id, objective=obj, order=idx))
    
    g1 = GrammarPoint(lesson_id=lesson.id, title="多少钱？- Hỏi giá", explanation="Dùng '多少钱？' (duō shao qián?) để hỏi 'Bao nhiêu tiền?' khi mua hàng", order=1)
    db.add(g1)
    db.flush()
    db.add(GrammarExample(grammar_point_id=g1.id, example="这个多少钱？(zhè ge duō shao qián?)", translation="Cái này bao nhiêu tiền?", order=1))
    db.add(GrammarExample(grammar_point_id=g1.id, example="一共多少钱？(yī gòng duō shao qián?)", translation="Tổng cộng bao nhiêu tiền?", order=2))
    
    g2 = GrammarPoint(lesson_id=lesson.id, title="太...了 - Quá...", explanation="Dùng '太...了' để diễn tả mức độ quá. Ví dụ: 太贵了 (quá đắt)", order=2)
    db.add(g2)
    db.flush()
    db.add(GrammarExample(grammar_point_id=g2.id, example="太贵了！(tài guì le!)", translation="Quá đắt!", order=1))
    db.add(GrammarExample(grammar_point_id=g2.id, example="太便宜了！(tài pián yi le!)", translation="Quá rẻ!", order=2))
    
    for i, ex in enumerate([
        {"question": "'Mua' trong tiếng Trung là gì?", "answer": "买", "options": '["买", "卖", "贵", "便宜"]'},
        {"question": "Dịch sang tiếng Trung: 'Bao nhiêu tiền?'", "answer": "多少钱？", "options": '[]'},
        {"question": "'便宜' có nghĩa là gì?", "answer": "rẻ", "options": '["rẻ", "đắt", "mua", "bán"]'},
        {"question": "Điền từ: 这个太___了！(Cái này quá đắt!)", "answer": "贵", "options": '["贵", "便宜", "好", "多"]'},
        {"question": "Dịch: 'Cửa hàng'", "answer": "商店", "options": '[]'},
    ]):
        db.add(Exercise(lesson_id=lesson.id, type="multiple_choice", order=i+1, **ex))
    
    db.commit()
    print("   [SUCCESS]")

# ============================================================================
# HSK 2.4 - DAILY ACTIVITIES
# ============================================================================
def seed_daily_activities(db):
    print("\n[HSK 2.4] Seeding Daily Activities...")
    lesson = db.query(Lesson).filter(Lesson.title == "Daily Activities", Lesson.hsk_level == 2).first()
    if not lesson:
        return
    
    clear_lesson_details(db, lesson)
    
    characters_data = [
        {"character": "起", "pinyin": "qǐ", "meaning": "dậy", "hsk_level": 2, "stroke_count": 10},
        {"character": "床", "pinyin": "chuáng", "meaning": "giường", "hsk_level": 2, "stroke_count": 7},
        {"character": "睡", "pinyin": "shuì", "meaning": "ngủ", "hsk_level": 2, "stroke_count": 13},
        {"character": "觉", "pinyin": "jiào", "meaning": "giấc (ngủ)", "hsk_level": 2, "stroke_count": 9},
        {"character": "吃", "pinyin": "chī", "meaning": "ăn", "hsk_level": 2, "stroke_count": 6},
        {"character": "饭", "pinyin": "fàn", "meaning": "cơm/bữa ăn", "hsk_level": 2, "stroke_count": 7},
        {"character": "喝", "pinyin": "hē", "meaning": "uống", "hsk_level": 2, "stroke_count": 12},
        {"character": "看", "pinyin": "kàn", "meaning": "xem/đọc", "hsk_level": 2, "stroke_count": 9},
        {"character": "书", "pinyin": "shū", "meaning": "sách", "hsk_level": 2, "stroke_count": 4},
        {"character": "作", "pinyin": "zuò", "meaning": "làm", "hsk_level": 2, "stroke_count": 7},
    ]
    add_characters_to_lesson(db, lesson, characters_data)
    
    vocab_items = [
        {"word": "起床", "pinyin": "qǐ chuáng", "meaning": "dậy (ngủ)", "example": "我七点起床。(wǒ qī diǎn qǐ chuáng) - Tôi dậy lúc 7 giờ.", "hsk_level": 2},
        {"word": "睡觉", "pinyin": "shuì jiào", "meaning": "đi ngủ", "example": "我十点睡觉。(wǒ shí diǎn shuì jiào) - Tôi ngủ lúc 10 giờ.", "hsk_level": 2},
        {"word": "吃饭", "pinyin": "chī fàn", "meaning": "ăn cơm", "example": "我们去吃饭。(wǒ men qù chī fàn) - Chúng ta đi ăn.", "hsk_level": 2},
        {"word": "喝水", "pinyin": "hē shuǐ", "meaning": "uống nước", "example": "多喝水 (duō hē shuǐ) - Uống nhiều nước", "hsk_level": 2},
        {"word": "看书", "pinyin": "kàn shū", "meaning": "đọc sách", "example": "我喜欢看书。(wǒ xǐ huan kàn shū) - Tôi thích đọc sách.", "hsk_level": 2},
        {"word": "工作", "pinyin": "gōng zuò", "meaning": "làm việc", "example": "去工作 (qù gōng zuò) - đi làm", "hsk_level": 2},
        {"word": "休息", "pinyin": "xiū xi", "meaning": "nghỉ ngơi", "example": "休息一下 (xiū xi yī xià) - nghỉ một chút", "hsk_level": 2},
        {"word": "洗澡", "pinyin": "xǐ zǎo", "meaning": "tắm", "example": "我要洗澡。(wǒ yào xǐ zǎo) - Tôi muốn tắm.", "hsk_level": 2},
        {"word": "运动", "pinyin": "yùn dòng", "meaning": "vận động/thể thao", "example": "喜欢运动 (xǐ huan yùn dòng) - thích thể thao", "hsk_level": 2},
        {"word": "学习", "pinyin": "xué xí", "meaning": "học tập", "example": "努力学习 (nǔ lì xué xí) - học hành chăm chỉ", "hsk_level": 2},
    ]
    add_vocabulary_to_lesson(db, lesson, vocab_items)
    
    for idx, obj in enumerate(["Học từ vựng về hoạt động hàng ngày", "Mô tả thói quen sinh hoạt", "Nói về lịch trình hàng ngày", "Sử dụng động từ kép"]):
        db.add(LessonObjective(lesson_id=lesson.id, objective=obj, order=idx))
    
    g1 = GrammarPoint(lesson_id=lesson.id, title="Động từ kép - Verb + Object", explanation="Nhiều hoạt động hàng ngày dùng động từ kép: 起床 (dậy), 睡觉 (ngủ), 吃饭 (ăn cơm), 看书 (đọc sách)", order=1)
    db.add(g1)
    db.flush()
    db.add(GrammarExample(grammar_point_id=g1.id, example="我每天七点起床。(wǒ měi tiān qī diǎn qǐ chuáng)", translation="Tôi dậy lúc 7 giờ mỗi ngày", order=1))
    db.add(GrammarExample(grammar_point_id=g1.id, example="晚上十点睡觉。(wǎn shang shí diǎn shuì jiào)", translation="Tối 10 giờ đi ngủ", order=2))
    
    for i, ex in enumerate([
        {"question": "'Dậy (ngủ)' trong tiếng Trung là gì?", "answer": "起床", "options": '["起床", "睡觉", "吃饭", "工作"]'},
        {"question": "Dịch sang tiếng Trung: 'Đi ngủ'", "answer": "睡觉", "options": '[]'},
        {"question": "'看书' có nghĩa là gì?", "answer": "đọc sách", "options": '["đọc sách", "xem TV", "viết", "học"]'},
        {"question": "Điền từ: 我七点___ (Tôi dậy lúc 7 giờ)", "answer": "起床", "options": '["起床", "睡觉", "上班", "下班"]'},
        {"question": "Dịch: 'Nghỉ ngơi'", "answer": "休息", "options": '[]'},
    ]):
        db.add(Exercise(lesson_id=lesson.id, type="multiple_choice", order=i+1, **ex))
    
    db.commit()
    print("   [SUCCESS]")

# ============================================================================
# HSK 2.5 - DIRECTIONS AND LOCATIONS
# ============================================================================
def seed_directions_and_locations(db):
    print("\n[HSK 2.5] Seeding Directions and Locations...")
    lesson = db.query(Lesson).filter(Lesson.title == "Directions and Locations", Lesson.hsk_level == 2).first()
    if not lesson:
        return
    
    clear_lesson_details(db, lesson)
    
    characters_data = [
        {"character": "左", "pinyin": "zuǒ", "meaning": "trái", "hsk_level": 2, "stroke_count": 5},
        {"character": "右", "pinyin": "yòu", "meaning": "phải", "hsk_level": 2, "stroke_count": 5},
        {"character": "前", "pinyin": "qián", "meaning": "trước", "hsk_level": 2, "stroke_count": 9},
        {"character": "后", "pinyin": "hòu", "meaning": "sau", "hsk_level": 2, "stroke_count": 6},
        {"character": "上", "pinyin": "shàng", "meaning": "trên", "hsk_level": 2, "stroke_count": 3},
        {"character": "下", "pinyin": "xià", "meaning": "dưới", "hsk_level": 2, "stroke_count": 3},
        {"character": "里", "pinyin": "lǐ", "meaning": "trong", "hsk_level": 2, "stroke_count": 7},
        {"character": "外", "pinyin": "wài", "meaning": "ngoài", "hsk_level": 2, "stroke_count": 5},
        {"character": "边", "pinyin": "biān", "meaning": "bên", "hsk_level": 2, "stroke_count": 5},
        {"character": "面", "pinyin": "miàn", "meaning": "mặt", "hsk_level": 2, "stroke_count": 9},
    ]
    add_characters_to_lesson(db, lesson, characters_data)
    
    vocab_items = [
        {"word": "左边", "pinyin": "zuǒ biān", "meaning": "bên trái", "example": "在左边 (zài zuǒ biān) - ở bên trái", "hsk_level": 2},
        {"word": "右边", "pinyin": "yòu biān", "meaning": "bên phải", "example": "在右边 (zài yòu biān) - ở bên phải", "hsk_level": 2},
        {"word": "前面", "pinyin": "qián miàn", "meaning": "phía trước", "example": "在前面 (zài qián miàn) - ở phía trước", "hsk_level": 2},
        {"word": "后面", "pinyin": "hòu miàn", "meaning": "phía sau", "example": "在后面 (zài hòu miàn) - ở phía sau", "hsk_level": 2},
        {"word": "上面", "pinyin": "shàng miàn", "meaning": "phía trên", "example": "在上面 (zài shàng miàn) - ở phía trên", "hsk_level": 2},
        {"word": "下面", "pinyin": "xià miàn", "meaning": "phía dưới", "example": "在下面 (zài xià miàn) - ở phía dưới", "hsk_level": 2},
        {"word": "里面", "pinyin": "lǐ miàn", "meaning": "bên trong", "example": "在里面 (zài lǐ miàn) - ở bên trong", "hsk_level": 2},
        {"word": "外面", "pinyin": "wài miàn", "meaning": "bên ngoài", "example": "在外面 (zài wài miàn) - ở bên ngoài", "hsk_level": 2},
        {"word": "旁边", "pinyin": "páng biān", "meaning": "bên cạnh", "example": "在旁边 (zài páng biān) - ở bên cạnh", "hsk_level": 2},
        {"word": "中间", "pinyin": "zhōng jiān", "meaning": "giữa", "example": "在中间 (zài zhōng jiān) - ở giữa", "hsk_level": 2},
    ]
    add_vocabulary_to_lesson(db, lesson, vocab_items)
    
    for idx, obj in enumerate(["Học từ vựng về phương hướng", "Chỉ đường", "Mô tả vị trí", "Hỏi đường"]):
        db.add(LessonObjective(lesson_id=lesson.id, objective=obj, order=idx))
    
    g1 = GrammarPoint(lesson_id=lesson.id, title="在 + phương hướng", explanation="Dùng 在 (zài) + phương hướng để chỉ vị trí. Ví dụ: 在左边 (ở bên trái), 在前面 (ở phía trước)", order=1)
    db.add(g1)
    db.flush()
    db.add(GrammarExample(grammar_point_id=g1.id, example="银行在左边。(yín háng zài zuǒ biān)", translation="Ngân hàng ở bên trái", order=1))
    db.add(GrammarExample(grammar_point_id=g1.id, example="学校在前面。(xué xiào zài qián miàn)", translation="Trường học ở phía trước", order=2))
    
    g2 = GrammarPoint(lesson_id=lesson.id, title="A在B的+方位", explanation="Mô tả vị trí tương đối: A + 在 + B + 的 + phương hướng", order=2)
    db.add(g2)
    db.flush()
    db.add(GrammarExample(grammar_point_id=g2.id, example="书在桌子上面。(shū zài zhuō zi shàng miàn)", translation="Sách ở trên bàn", order=1))
    db.add(GrammarExample(grammar_point_id=g2.id, example="猫在椅子下面。(māo zài yǐ zi xià miàn)", translation="Mèo ở dưới ghế", order=2))
    
    for i, ex in enumerate([
        {"question": "'Bên trái' trong tiếng Trung là gì?", "answer": "左边", "options": '["左边", "右边", "前面", "后面"]'},
        {"question": "Dịch sang tiếng Trung: 'Ở phía trên'", "answer": "在上面", "options": '[]'},
        {"question": "'里面' có nghĩa là gì?", "answer": "bên trong", "options": '["bên trong", "bên ngoài", "bên cạnh", "giữa"]'},
        {"question": "Điền từ: 银行在___ (Ngân hàng ở bên phải)", "answer": "右边", "options": '["右边", "左边", "前面", "后面"]'},
        {"question": "Dịch: 'Ở giữa'", "answer": "在中间", "options": '[]'},
    ]):
        db.add(Exercise(lesson_id=lesson.id, type="multiple_choice", order=i+1, **ex))
    
    db.commit()
    print("   [SUCCESS]")

# ============================================================================
# HSK 2.6 - FOOD AND DINING
# ============================================================================
def seed_food_and_dining(db):
    print("\n[HSK 2.6] Seeding Food and Dining...")
    lesson = db.query(Lesson).filter(Lesson.title == "Food and Dining", Lesson.hsk_level == 2).first()
    if not lesson:
        return
    
    clear_lesson_details(db, lesson)
    
    characters_data = [
        {"character": "饭", "pinyin": "fàn", "meaning": "cơm/bữa ăn", "hsk_level": 2, "stroke_count": 7},
        {"character": "菜", "pinyin": "cài", "meaning": "món ăn/rau", "hsk_level": 2, "stroke_count": 11},
        {"character": "肉", "pinyin": "ròu", "meaning": "thịt", "hsk_level": 2, "stroke_count": 6},
        {"character": "鱼", "pinyin": "yú", "meaning": "cá", "hsk_level": 2, "stroke_count": 8},
        {"character": "茶", "pinyin": "chá", "meaning": "trà", "hsk_level": 2, "stroke_count": 9},
        {"character": "酒", "pinyin": "jiǔ", "meaning": "rượu", "hsk_level": 2, "stroke_count": 10},
        {"character": "味", "pinyin": "wèi", "meaning": "vị", "hsk_level": 2, "stroke_count": 8},
        {"character": "饿", "pinyin": "è", "meaning": "đói", "hsk_level": 2, "stroke_count": 10},
        {"character": "渴", "pinyin": "kě", "meaning": "khát", "hsk_level": 2, "stroke_count": 12},
        {"character": "果", "pinyin": "guǒ", "meaning": "quả", "hsk_level": 2, "stroke_count": 8},
    ]
    add_characters_to_lesson(db, lesson, characters_data)
    
    vocab_items = [
        {"word": "米饭", "pinyin": "mǐ fàn", "meaning": "cơm", "example": "我要米饭。(wǒ yào mǐ fàn) - Tôi muốn cơm.", "hsk_level": 2},
        {"word": "菜", "pinyin": "cài", "meaning": "món ăn", "example": "点菜 (diǎn cài) - gọi món", "hsk_level": 2},
        {"word": "肉", "pinyin": "ròu", "meaning": "thịt", "example": "牛肉 (niú ròu) - thịt bò", "hsk_level": 2},
        {"word": "鱼", "pinyin": "yú", "meaning": "cá", "example": "吃鱼 (chī yú) - ăn cá", "hsk_level": 2},
        {"word": "水果", "pinyin": "shuǐ guǒ", "meaning": "trái cây", "example": "买水果 (mǎi shuǐ guǒ) - mua trái cây", "hsk_level": 2},
        {"word": "茶", "pinyin": "chá", "meaning": "trà", "example": "喝茶 (hē chá) - uống trà", "hsk_level": 2},
        {"word": "好吃", "pinyin": "hǎo chī", "meaning": "ngon", "example": "很好吃！(hěn hǎo chī!) - Rất ngon!", "hsk_level": 2},
        {"word": "饿", "pinyin": "è", "meaning": "đói", "example": "我饿了。(wǒ è le) - Tôi đói rồi.", "hsk_level": 2},
        {"word": "渴", "pinyin": "kě", "meaning": "khát", "example": "我渴了。(wǒ kě le) - Tôi khát rồi.", "hsk_level": 2},
        {"word": "餐厅", "pinyin": "cān tīng", "meaning": "nhà hàng", "example": "去餐厅 (qù cān tīng) - đi nhà hàng", "hsk_level": 2},
    ]
    add_vocabulary_to_lesson(db, lesson, vocab_items)
    
    for idx, obj in enumerate(["Học từ vựng về đồ ăn", "Gọi món ăn tại nhà hàng", "Mô tả vị của món ăn", "Diễn tả cảm giác đói khát"]):
        db.add(LessonObjective(lesson_id=lesson.id, objective=obj, order=idx))
    
    g1 = GrammarPoint(lesson_id=lesson.id, title="好吃/好喝 - Ngon", explanation="Dùng 好吃 cho đồ ăn ngon, 好喝 cho đồ uống ngon", order=1)
    db.add(g1)
    db.flush()
    db.add(GrammarExample(grammar_point_id=g1.id, example="这个菜很好吃。(zhè ge cài hěn hǎo chī)", translation="Món này ngon", order=1))
    db.add(GrammarExample(grammar_point_id=g1.id, example="这个茶很好喝。(zhè ge chá hěn hǎo hē)", translation="Trà này ngon", order=2))
    
    g2 = GrammarPoint(lesson_id=lesson.id, title="...了 - Biểu thị trạng thái mới", explanation="Dùng 了 sau tính từ để biểu thị trạng thái thay đổi: 饿了 (đói rồi), 渴了 (khát rồi)", order=2)
    db.add(g2)
    db.flush()
    db.add(GrammarExample(grammar_point_id=g2.id, example="我饿了，我们吃饭吧。(wǒ è le, wǒ men chī fàn ba)", translation="Tôi đói rồi, chúng ta ăn đi", order=1))
    db.add(GrammarExample(grammar_point_id=g2.id, example="我渴了，要喝水。(wǒ kě le, yào hē shuǐ)", translation="Tôi khát rồi, muốn uống nước", order=2))
    
    for i, ex in enumerate([
        {"question": "'Ngon' (cho đồ ăn) trong tiếng Trung là gì?", "answer": "好吃", "options": '["好吃", "好喝", "饿", "渴"]'},
        {"question": "Dịch sang tiếng Trung: 'Tôi đói rồi'", "answer": "我饿了", "options": '[]'},
        {"question": "'鱼' có nghĩa là gì?", "answer": "cá", "options": '["cá", "thịt", "rau", "cơm"]'},
        {"question": "Điền từ: 这个菜很___ (Món này ngon)", "answer": "好吃", "options": '["好吃", "好喝", "饿", "渴"]'},
        {"question": "Dịch: 'Nhà hàng'", "answer": "餐厅", "options": '[]'},
    ]):
        db.add(Exercise(lesson_id=lesson.id, type="multiple_choice", order=i+1, **ex))
    
    db.commit()
    print("   [SUCCESS]")

# ============================================================================
# MAIN FUNCTION
# ============================================================================
def seed_all_hsk2_lessons():
    db = SessionLocal()
    
    try:
        print("=" * 80)
        print("Seeding All HSK 2 Lesson Details...")
        print("=" * 80)
        
        seed_time_and_date(db)
        seed_weather_and_seasons(db)
        seed_shopping_and_money(db)
        seed_daily_activities(db)
        seed_directions_and_locations(db)
        seed_food_and_dining(db)
        
        print("\n" + "=" * 80)
        print("[SUCCESS] All HSK 2 lessons seeded!")
        print("=" * 80)
        
        hsk2_lessons = db.query(Lesson).filter(Lesson.hsk_level == 2).all()
        print(f"\nTotal HSK 2 Lessons: {len(hsk2_lessons)}")
        for lesson in hsk2_lessons:
            print(f"\n{lesson.title}:")
            print(f"  - Characters: {len(lesson.characters)}")
            print(f"  - Vocabulary: {len(lesson.vocabularies)}")
            print(f"  - Objectives: {len(lesson.objectives)}")
            print(f"  - Grammar: {len(lesson.grammar_points)}")
            print(f"  - Exercises: {len(lesson.exercises)}")
        
        print("\n" + "=" * 80)
        print("Test API:")
        print("  curl http://localhost:8000/api/lessons?hsk_level=2")
        for lesson in hsk2_lessons:
            print(f"  curl http://localhost:8000/api/lessons/{lesson.id}")
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