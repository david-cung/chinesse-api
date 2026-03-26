"""
Seed script to add missing vocabulary and units for HSK 3 and 4 (Lessons 1-6)
"""
import sys
import os
sys.path.append('.')

from database.database import SessionLocal
from models.lesson import Lesson, Vocabulary
from models.unit import Unit
from models.character import Character
from models.sentence import Sentence

# HSK 3 Lessons 1-6 Data
HSK3_CONTENT = {
    1: [ # Hobbies and Interests
        {"word": "爱好", "pinyin": "àihào", "meaning": "sở thích"},
        {"word": "经常", "pinyin": "jīngcháng", "meaning": "thường xuyên"},
        {"word": "踢足球", "pinyin": "tī zúqiú", "meaning": "đá bóng"},
        {"word": "游泳", "pinyin": "yóuyǒng", "meaning": "bơi lội"},
        {"word": "旅游", "pinyin": "lǚyóu", "meaning": "du lịch"},
        {"word": "电影", "pinyin": "diànyǐng", "meaning": "phim"},
        {"word": "音乐", "pinyin": "yīnyuè", "meaning": "âm nhạc"},
        {"word": "已经", "pinyin": "yǐjīng", "meaning": "đã"},
    ],
    2: [ # Travel and Transportation
        {"word": "宾馆", "pinyin": "bīnguǎn", "meaning": "khách sạn"},
        {"word": "护照", "pinyin": "hùzhào", "meaning": "hộ chiếu"},
        {"word": "票", "pinyin": "piào", "meaning": "vé"},
        {"word": "行李", "pinyin": "xíngli", "meaning": "hành lý"},
        {"word": "行李托运", "pinyin": "xíngli tuōyùn", "meaning": "ký gửi hành lý"},
        {"word": "登机牌", "pinyin": "dēngjīpái", "meaning": "thẻ lên máy bay"},
        {"word": "晚点", "pinyin": "wǎndiǎn", "meaning": "trễ giờ"},
        {"word": "取消", "pinyin": "qǔxiāo", "meaning": "hủy bỏ"},
    ],
    3: [ # Health and Medical
        {"word": "生病", "pinyin": "shēngbìng", "meaning": "bị bệnh"},
        {"word": "医生", "pinyin": "yīshēng", "meaning": "bác sĩ"},
        {"word": "吃药", "pinyin": "chī yào", "meaning": "uống thuốc"},
        {"word": "感冒", "pinyin": "gǎnmào", "meaning": "cảm cúm"},
        {"word": "发烧", "pinyin": "fāshāo", "meaning": "sốt"},
        {"word": "嗓子", "pinyin": "sǎngzi", "meaning": "họng"},
        {"word": "检查", "pinyin": "jiǎnchá", "meaning": "kiểm tra"},
        {"word": "休息", "pinyin": "xiūxi", "meaning": "nghỉ ngơi"},
    ],
    4: [ # Making Plans
        {"word": "打算", "pinyin": "dǎsuàn", "meaning": "dự định"},
        {"word": "安排", "pinyin": "ānpái", "meaning": "sắp xếp"},
        {"word": "参加", "pinyin": "cānjiā", "meaning": "tham gia"},
        {"word": "准时", "pinyin": "zhǔnshí", "meaning": "đúng giờ"},
        {"word": "准备", "pinyin": "zhǔnbèi", "meaning": "chuẩn bị"},
        {"word": "主意", "pinyin": "zhǔyi", "meaning": "ý kiến"},
        {"word": "会议", "pinyin": "huìyì", "meaning": "cuộc họp"},
        {"word": "周末", "pinyin": "zhōumò", "meaning": "cuối tuần"},
    ],
    5: [ # Describing People
        {"word": "聪明", "pinyin": "cōngming", "meaning": "thông minh"},
        {"word": "性格", "pinyin": "xìnggé", "meaning": "tính cách"},
        {"word": "瘦", "pinyin": "shòu", "meaning": "gầy"},
        {"word": "胖", "pinyin": "pàng", "meaning": "béo"},
        {"word": "个子", "pinyin": "gèzi", "meaning": "dáng người (chiều cao)"},
        {"word": "认真", "pinyin": "rènzhēn", "meaning": "chăm chỉ/nghiêm túc"},
        {"word": "热情", "pinyin": "rèqíng", "meaning": "nhiệt tình"},
        {"word": "像", "pinyin": "xiàng", "meaning": "giống"},
    ],
    6: [ # Life Events
        {"word": "毕业", "pinyin": "bìyè", "meaning": "tốt nghiệp"},
        {"word": "打算", "pinyin": "dǎsuàn", "meaning": "dự định"},
        {"word": "找工作", "pinyin": "zhǎo gōngzuò", "meaning": "tìm việc"},
        {"word": "搬家", "pinyin": "bānjiā", "meaning": "chuyển nhà"},
        {"word": "结束", "pinyin": "jiéshù", "meaning": "kết thúc"},
        {"word": "结婚", "pinyin": "jiéhūn", "meaning": "kết hôn"},
        {"word": "决定", "pinyin": "juédìng", "meaning": "quyết định"},
        {"word": "快乐", "pinyin": "kuàilè", "meaning": "vui vẻ/hạnh phúc"},
    ],
}

# HSK 4 Lessons 1-6 Data
HSK4_CONTENT = {
    1: [ # Work and Career
        {"word": "面试", "pinyin": "miànshì", "meaning": "phỏng vấn"},
        {"word": "简历", "pinyin": "jiǎnlì", "meaning": "sơ yếu lý lịch"},
        {"word": "招聘", "pinyin": "zhāopìn", "meaning": "tuyển dụng"},
        {"word": "负责人", "pinyin": "fùzérén", "meaning": "người phụ trách"},
        {"word": "积累", "pinyin": "jīlěi", "meaning": "tích lũy"},
        {"word": "经验", "pinyin": "jīngyàn", "meaning": "kinh nghiệm"},
        {"word": "工资", "pinyin": "gōngzī", "meaning": "lương"},
        {"word": "顺利", "pinyin": "shùnlì", "meaning": "thuận lợi"},
    ],
    2: [ # Technology and Internet
        {"word": "软件", "pinyin": "ruǎnjiàn", "meaning": "phần mềm"},
        {"word": "下载", "pinyin": "xiàzǎi", "meaning": "tải xuống"},
        {"word": "密码", "pinyin": "mìmǎ", "meaning": "mật khẩu"},
        {"word": "账号", "pinyin": "zhànghào", "meaning": "tài khoản"},
        {"word": "视频", "pinyin": "shìpín", "meaning": "video"},
        {"word": "互联网", "pinyin": "hùliánwǎng", "meaning": "mạng internet"},
        {"word": "方便", "pinyin": "fāngbiàn", "meaning": "tiện lợi"},
        {"word": "更新", "pinyin": "gēngxīn", "meaning": "cập nhật"},
    ],
    3: [ # Society and Culture
        {"word": "风俗", "pinyin": "fēngsú", "meaning": "phong tục"},
        {"word": "传统", "pinyin": "chuántǒng", "meaning": "truyền thống"},
        {"word": "关系", "pinyin": "guānxì", "meaning": "quan hệ"},
        {"word": "信任", "pinyin": "xìnrèn", "meaning": "tin tưởng"},
        {"word": "重视", "pinyin": "zhòngshì", "meaning": "coi trọng"},
        {"word": "法律", "pinyin": "fǎlǜ", "meaning": "pháp luật"},
        {"word": "坚持", "pinyin": "jiānchí", "meaning": "kiên trì"},
        {"word": "理解", "pinyin": "lǐjiě", "meaning": "hiểu/lý giải"},
    ],
    4: [ # Education and Learning
        {"word": "奖学金", "pinyin": "jiǎngxuéjīn", "meaning": "học bổng"},
        {"word": "硕士", "pinyin": "shuòshì", "meaning": "thạc sĩ"},
        {"word": "博士", "pinyin": "bóshì", "meaning": "tiến sĩ"},
        {"word": "论文", "pinyin": "lùnwén", "meaning": "luận văn"},
        {"word": "研究", "pinyin": "yánjiū", "meaning": "nghiên cứu"},
        {"word": "由于", "pinyin": "yóuyú", "meaning": "do là/bởi vì"},
        {"word": "提高", "pinyin": "tígāo", "meaning": "nâng cao"},
        {"word": "知识", "pinyin": "zhīshi", "meaning": "kiến thức"},
    ],
    5: [ # Environment and Nature
        {"word": "垃圾", "pinyin": "lājī", "meaning": "rác"},
        {"word": "污染", "pinyin": "wūrǎn", "meaning": "ô nhiễm"},
        {"word": "保护", "pinyin": "bǎohù", "meaning": "bảo vệ"},
        {"word": "节约", "pinyin": "jiéyuē", "meaning": "tiết kiệm"},
        {"word": "气候", "pinyin": "qìhòu", "meaning": "khí hậu"},
        {"word": "变暖", "pinyin": "biànnuǎn", "meaning": "trở nên ấm lên"},
        {"word": "大自然", "pinyin": "dàzìrán", "meaning": "thiên nhiên"},
        {"word": "意识", "pinyin": "yìshí", "meaning": "ý thức"},
    ],
    6: [ # News and Media
        {"word": "新闻", "pinyin": "xīnwén", "meaning": "tin tức"},
        {"word": "记者", "pinyin": "jìzhě", "meaning": "phóng viên"},
        {"word": "报道", "pinyin": "bàodào", "meaning": "báo cáo/đưa tin"},
        {"word": "发布", "pinyin": "fābù", "meaning": "công bố"},
        {"word": "消息", "pinyin": "xiāoxi", "meaning": "thông tin/tin tức"},
        {"word": "交流", "pinyin": "jiāoliú", "meaning": "giao lưu"},
        {"word": "精彩", "pinyin": "jīngcǎi", "meaning": "tuyệt vời/đặc sắc"},
        {"word": "观众", "pinyin": "guānzhòng", "meaning": "khán giả"},
    ],
}

def seed_missing_content():
    db = SessionLocal()
    try:
        # Loop through levels
        for level, content in [(3, HSK3_CONTENT), (4, HSK4_CONTENT)]:
            print(f"Populating HSK {level} Lessons 1-6...")
            for order, vocab_list in content.items():
                lesson = db.query(Lesson).filter(Lesson.hsk_level == level, Lesson.order == order).first()
                if not lesson:
                    print(f"  Lesson {order} not found at level {level}, skipping.")
                    continue
                
                print(f"  Processing Lesson {order}: {lesson.title}")
                
                # Create Units if they don't exist
                existing_units = db.query(Unit).filter(Unit.lesson_id == lesson.id).all()
                if not existing_units:
                    default_units = [
                        {"type": "vocabulary", "title": "Học từ vựng", "order": 1, "duration_minutes": 5},
                        {"type": "listening", "title": "Nghe hiểu", "order": 2, "duration_minutes": 5},
                        {"type": "speaking", "title": "Luyện nói", "order": 3, "duration_minutes": 5},
                        {"type": "exercise", "title": "Bài tập", "order": 4, "duration_minutes": 5},
                    ]
                    for ud in default_units:
                        unit = Unit(lesson_id=lesson.id, **ud)
                        db.add(unit)
                
                # Add vocabularies
                for v_data in vocab_list:
                    # Check if vocabulary already exists
                    vocab = db.query(Vocabulary).filter(Vocabulary.word == v_data["word"]).first()
                    if not vocab:
                        vocab = Vocabulary(**v_data, hsk_level=level)
                        db.add(vocab)
                        db.flush()
                    
                    # Link to lesson if not already linked
                    if vocab not in lesson.vocabularies:
                        lesson.vocabularies.append(vocab)
            
            db.commit()
            print(f"Completed HSK {level}.")
        
        print("Success: All missing content seeded!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding content: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    seed_missing_content()
