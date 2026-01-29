"""
Seed script để thêm câu mẫu cho từ vựng HSK1
Chạy: PYTHONPATH=/Users/dc/Documents/code/tian-tian-backend python seed/seed_vocabulary_examples.py
"""
import sys
sys.path.insert(0, '/Users/dc/Documents/code/tian-tian-backend')

from database.database import SessionLocal, engine, Base
from models.lesson import Vocabulary, VocabularyExample

# Tạo bảng mới nếu chưa có
Base.metadata.create_all(bind=engine)

# Dữ liệu câu mẫu cho từ vựng phổ biến HSK1
VOCABULARY_EXAMPLES = {
    "你好": [
        {
            "sentence": "你好，我是小明。",
            "pinyin": "Nǐ hǎo, wǒ shì Xiǎo Míng.",
            "translation": "Xin chào, tôi là Tiểu Minh."
        },
        {
            "sentence": "你好吗？",
            "pinyin": "Nǐ hǎo ma?",
            "translation": "Bạn khỏe không?"
        }
    ],
    "谢谢": [
        {
            "sentence": "谢谢你的帮助。",
            "pinyin": "Xièxiè nǐ de bāngzhù.",
            "translation": "Cảm ơn sự giúp đỡ của bạn."
        },
        {
            "sentence": "非常谢谢！",
            "pinyin": "Fēicháng xièxiè!",
            "translation": "Cảm ơn rất nhiều!"
        }
    ],
    "再见": [
        {
            "sentence": "明天见，再见！",
            "pinyin": "Míngtiān jiàn, zàijiàn!",
            "translation": "Mai gặp lại, tạm biệt!"
        }
    ],
    "我": [
        {
            "sentence": "我是学生。",
            "pinyin": "Wǒ shì xuéshēng.",
            "translation": "Tôi là học sinh."
        },
        {
            "sentence": "我很高兴。",
            "pinyin": "Wǒ hěn gāoxìng.",
            "translation": "Tôi rất vui."
        }
    ],
    "你": [
        {
            "sentence": "你叫什么名字？",
            "pinyin": "Nǐ jiào shénme míngzì?",
            "translation": "Bạn tên là gì?"
        },
        {
            "sentence": "你是哪国人？",
            "pinyin": "Nǐ shì nǎ guó rén?",
            "translation": "Bạn là người nước nào?"
        }
    ],
    "他": [
        {
            "sentence": "他是我的朋友。",
            "pinyin": "Tā shì wǒ de péngyǒu.",
            "translation": "Anh ấy là bạn của tôi."
        }
    ],
    "她": [
        {
            "sentence": "她很漂亮。",
            "pinyin": "Tā hěn piàoliang.",
            "translation": "Cô ấy rất đẹp."
        }
    ],
    "是": [
        {
            "sentence": "这是我的书。",
            "pinyin": "Zhè shì wǒ de shū.",
            "translation": "Đây là sách của tôi."
        },
        {
            "sentence": "他是老师。",
            "pinyin": "Tā shì lǎoshī.",
            "translation": "Anh ấy là giáo viên."
        }
    ],
    "不": [
        {
            "sentence": "我不是医生。",
            "pinyin": "Wǒ bù shì yīshēng.",
            "translation": "Tôi không phải là bác sĩ."
        },
        {
            "sentence": "他不吃肉。",
            "pinyin": "Tā bù chī ròu.",
            "translation": "Anh ấy không ăn thịt."
        }
    ],
    "好": [
        {
            "sentence": "今天天气很好。",
            "pinyin": "Jīntiān tiānqì hěn hǎo.",
            "translation": "Hôm nay thời tiết rất tốt."
        },
        {
            "sentence": "好的，没问题。",
            "pinyin": "Hǎo de, méi wèntí.",
            "translation": "Được, không vấn đề gì."
        }
    ],
    "请": [
        {
            "sentence": "请进！",
            "pinyin": "Qǐng jìn!",
            "translation": "Mời vào!"
        },
        {
            "sentence": "请坐。",
            "pinyin": "Qǐng zuò.",
            "translation": "Mời ngồi."
        }
    ],
    "对不起": [
        {
            "sentence": "对不起，我迟到了。",
            "pinyin": "Duìbùqǐ, wǒ chídào le.",
            "translation": "Xin lỗi, tôi đến muộn."
        }
    ],
    "没关系": [
        {
            "sentence": "没关系，不用担心。",
            "pinyin": "Méi guānxi, bùyòng dānxīn.",
            "translation": "Không sao, đừng lo lắng."
        }
    ],
    "爸爸": [
        {
            "sentence": "我爸爸是工程师。",
            "pinyin": "Wǒ bàba shì gōngchéngshī.",
            "translation": "Bố tôi là kỹ sư."
        }
    ],
    "妈妈": [
        {
            "sentence": "妈妈做的菜很好吃。",
            "pinyin": "Māma zuò de cài hěn hǎochī.",
            "translation": "Món ăn mẹ nấu rất ngon."
        }
    ],
    "朋友": [
        {
            "sentence": "我们是好朋友。",
            "pinyin": "Wǒmen shì hǎo péngyǒu.",
            "translation": "Chúng tôi là bạn tốt."
        }
    ],
    "老师": [
        {
            "sentence": "老师正在上课。",
            "pinyin": "Lǎoshī zhèngzài shàngkè.",
            "translation": "Thầy giáo đang giảng bài."
        }
    ],
    "学生": [
        {
            "sentence": "我是大学生。",
            "pinyin": "Wǒ shì dàxuéshēng.",
            "translation": "Tôi là sinh viên đại học."
        }
    ],
    "吃": [
        {
            "sentence": "我喜欢吃中国菜。",
            "pinyin": "Wǒ xǐhuān chī Zhōngguó cài.",
            "translation": "Tôi thích ăn món Trung Quốc."
        }
    ],
    "喝": [
        {
            "sentence": "你想喝什么？",
            "pinyin": "Nǐ xiǎng hē shénme?",
            "translation": "Bạn muốn uống gì?"
        }
    ],
    "水": [
        {
            "sentence": "请给我一杯水。",
            "pinyin": "Qǐng gěi wǒ yī bēi shuǐ.",
            "translation": "Làm ơn cho tôi một cốc nước."
        }
    ],
    "茶": [
        {
            "sentence": "中国茶很有名。",
            "pinyin": "Zhōngguó chá hěn yǒumíng.",
            "translation": "Trà Trung Quốc rất nổi tiếng."
        }
    ],
    "咖啡": [
        {
            "sentence": "我每天早上喝咖啡。",
            "pinyin": "Wǒ měitiān zǎoshang hē kāfēi.",
            "translation": "Tôi uống cà phê mỗi sáng."
        }
    ],
    "米饭": [
        {
            "sentence": "中国人喜欢吃米饭。",
            "pinyin": "Zhōngguó rén xǐhuān chī mǐfàn.",
            "translation": "Người Trung Quốc thích ăn cơm."
        }
    ],
    "一": [
        {
            "sentence": "我有一个问题。",
            "pinyin": "Wǒ yǒu yī gè wèntí.",
            "translation": "Tôi có một câu hỏi."
        }
    ],
    "二": [
        {
            "sentence": "我有两个孩子。",
            "pinyin": "Wǒ yǒu liǎng gè háizi.",
            "translation": "Tôi có hai đứa con."
        }
    ],
    "三": [
        {
            "sentence": "现在三点钟。",
            "pinyin": "Xiànzài sān diǎn zhōng.",
            "translation": "Bây giờ là ba giờ."
        }
    ],
    "今天": [
        {
            "sentence": "今天是星期一。",
            "pinyin": "Jīntiān shì xīngqī yī.",
            "translation": "Hôm nay là thứ Hai."
        }
    ],
    "明天": [
        {
            "sentence": "明天我们去北京。",
            "pinyin": "Míngtiān wǒmen qù Běijīng.",
            "translation": "Ngày mai chúng tôi đi Bắc Kinh."
        }
    ],
    "昨天": [
        {
            "sentence": "昨天我去看电影了。",
            "pinyin": "Zuótiān wǒ qù kàn diànyǐng le.",
            "translation": "Hôm qua tôi đi xem phim."
        }
    ]
}


def seed_vocabulary_examples():
    db = SessionLocal()
    try:
        added_count = 0
        
        for word, examples in VOCABULARY_EXAMPLES.items():
            # Tìm từ vựng trong database
            vocab = db.query(Vocabulary).filter(Vocabulary.word == word).first()
            
            if vocab:
                # Kiểm tra xem đã có câu mẫu chưa
                existing = db.query(VocabularyExample).filter(
                    VocabularyExample.vocabulary_id == vocab.id
                ).count()
                
                if existing == 0:
                    for order, ex_data in enumerate(examples, 1):
                        example = VocabularyExample(
                            vocabulary_id=vocab.id,
                            sentence=ex_data["sentence"],
                            pinyin=ex_data.get("pinyin"),
                            translation=ex_data.get("translation"),
                            order=order
                        )
                        db.add(example)
                        added_count += 1
                    print(f"✅ Added {len(examples)} examples for '{word}'")
                else:
                    print(f"⏭️  Skipped '{word}' (already has {existing} examples)")
            else:
                print(f"⚠️  Vocabulary '{word}' not found in database")
        
        db.commit()
        print(f"\n🎉 Successfully added {added_count} vocabulary examples!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_vocabulary_examples()
