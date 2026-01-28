"""
Seed script to add lessons for HSK 2, 3, 4, 5
Each level should have 14 lessons total
"""
from database.database import SessionLocal
from models.lesson import Lesson, Vocabulary, LessonObjective
from models.unit import Unit

# HSK 2 Topics (intermediate beginner)
HSK2_LESSONS = [
    {"title": "Bài 7: Sở thích", "description": "Nói về các sở thích và hoạt động yêu thích", "estimated_time": 12,
     "vocabularies": [
         {"word": "运动", "pinyin": "yùndòng", "meaning": "thể thao"},
         {"word": "音乐", "pinyin": "yīnyuè", "meaning": "âm nhạc"},
         {"word": "电影", "pinyin": "diànyǐng", "meaning": "phim"},
         {"word": "旅游", "pinyin": "lǚyóu", "meaning": "du lịch"},
         {"word": "游泳", "pinyin": "yóuyǒng", "meaning": "bơi lội"},
         {"word": "跑步", "pinyin": "pǎobù", "meaning": "chạy bộ"},
         {"word": "唱歌", "pinyin": "chànggē", "meaning": "hát"},
         {"word": "跳舞", "pinyin": "tiàowǔ", "meaning": "nhảy múa"},
     ]},
    {"title": "Bài 8: Đi mua sắm", "description": "Học cách mua sắm và trả giá", "estimated_time": 12,
     "vocabularies": [
         {"word": "商场", "pinyin": "shāngchǎng", "meaning": "trung tâm thương mại"},
         {"word": "超市", "pinyin": "chāoshì", "meaning": "siêu thị"},
         {"word": "衣服", "pinyin": "yīfu", "meaning": "quần áo"},
         {"word": "鞋子", "pinyin": "xiézi", "meaning": "giày"},
         {"word": "试穿", "pinyin": "shìchuān", "meaning": "thử đồ"},
         {"word": "打折", "pinyin": "dǎzhé", "meaning": "giảm giá"},
         {"word": "现金", "pinyin": "xiànjīn", "meaning": "tiền mặt"},
         {"word": "信用卡", "pinyin": "xìnyòngkǎ", "meaning": "thẻ tín dụng"},
     ]},
    {"title": "Bài 9: Đặt phòng khách sạn", "description": "Học cách đặt phòng và sử dụng dịch vụ khách sạn", "estimated_time": 12,
     "vocabularies": [
         {"word": "酒店", "pinyin": "jiǔdiàn", "meaning": "khách sạn"},
         {"word": "预订", "pinyin": "yùdìng", "meaning": "đặt trước"},
         {"word": "房间", "pinyin": "fángjiān", "meaning": "phòng"},
         {"word": "钥匙", "pinyin": "yàoshi", "meaning": "chìa khóa"},
         {"word": "退房", "pinyin": "tuìfáng", "meaning": "trả phòng"},
         {"word": "服务员", "pinyin": "fúwùyuán", "meaning": "nhân viên"},
         {"word": "空调", "pinyin": "kōngtiáo", "meaning": "điều hòa"},
         {"word": "早餐", "pinyin": "zǎocān", "meaning": "bữa sáng"},
     ]},
    {"title": "Bài 10: Phương hướng", "description": "Hỏi đường và chỉ đường", "estimated_time": 12,
     "vocabularies": [
         {"word": "东", "pinyin": "dōng", "meaning": "đông"},
         {"word": "西", "pinyin": "xī", "meaning": "tây"},
         {"word": "南", "pinyin": "nán", "meaning": "nam"},
         {"word": "北", "pinyin": "běi", "meaning": "bắc"},
         {"word": "左", "pinyin": "zuǒ", "meaning": "trái"},
         {"word": "右", "pinyin": "yòu", "meaning": "phải"},
         {"word": "前面", "pinyin": "qiánmiàn", "meaning": "phía trước"},
         {"word": "后面", "pinyin": "hòumiàn", "meaning": "phía sau"},
     ]},
    {"title": "Bài 11: Gọi món ăn", "description": "Học cách gọi món tại nhà hàng", "estimated_time": 12,
     "vocabularies": [
         {"word": "菜单", "pinyin": "càidān", "meaning": "thực đơn"},
         {"word": "点菜", "pinyin": "diǎncài", "meaning": "gọi món"},
         {"word": "饮料", "pinyin": "yǐnliào", "meaning": "đồ uống"},
         {"word": "服务员", "pinyin": "fúwùyuán", "meaning": "phục vụ"},
         {"word": "买单", "pinyin": "mǎidān", "meaning": "tính tiền"},
         {"word": "辣", "pinyin": "là", "meaning": "cay"},
         {"word": "甜", "pinyin": "tián", "meaning": "ngọt"},
         {"word": "咸", "pinyin": "xián", "meaning": "mặn"},
     ]},
    {"title": "Bài 12: Sức khỏe", "description": "Nói về sức khỏe và đi khám bệnh", "estimated_time": 12,
     "vocabularies": [
         {"word": "生病", "pinyin": "shēngbìng", "meaning": "bị bệnh"},
         {"word": "感冒", "pinyin": "gǎnmào", "meaning": "cảm cúm"},
         {"word": "发烧", "pinyin": "fāshāo", "meaning": "sốt"},
         {"word": "头疼", "pinyin": "tóuténg", "meaning": "đau đầu"},
         {"word": "医生", "pinyin": "yīshēng", "meaning": "bác sĩ"},
         {"word": "药", "pinyin": "yào", "meaning": "thuốc"},
         {"word": "休息", "pinyin": "xiūxi", "meaning": "nghỉ ngơi"},
         {"word": "健康", "pinyin": "jiànkāng", "meaning": "khỏe mạnh"},
     ]},
    {"title": "Bài 13: Thể thao", "description": "Các môn thể thao phổ biến", "estimated_time": 12,
     "vocabularies": [
         {"word": "足球", "pinyin": "zúqiú", "meaning": "bóng đá"},
         {"word": "篮球", "pinyin": "lánqiú", "meaning": "bóng rổ"},
         {"word": "网球", "pinyin": "wǎngqiú", "meaning": "tennis"},
         {"word": "乒乓球", "pinyin": "pīngpāngqiú", "meaning": "bóng bàn"},
         {"word": "比赛", "pinyin": "bǐsài", "meaning": "thi đấu"},
         {"word": "赢", "pinyin": "yíng", "meaning": "thắng"},
         {"word": "输", "pinyin": "shū", "meaning": "thua"},
         {"word": "练习", "pinyin": "liànxí", "meaning": "luyện tập"},
     ]},
    {"title": "Bài 14: Kế hoạch tương lai", "description": "Nói về dự định và kế hoạch", "estimated_time": 12,
     "vocabularies": [
         {"word": "计划", "pinyin": "jìhuà", "meaning": "kế hoạch"},
         {"word": "打算", "pinyin": "dǎsuàn", "meaning": "dự định"},
         {"word": "希望", "pinyin": "xīwàng", "meaning": "hy vọng"},
         {"word": "将来", "pinyin": "jiānglái", "meaning": "tương lai"},
         {"word": "目标", "pinyin": "mùbiāo", "meaning": "mục tiêu"},
         {"word": "准备", "pinyin": "zhǔnbèi", "meaning": "chuẩn bị"},
         {"word": "决定", "pinyin": "juédìng", "meaning": "quyết định"},
         {"word": "成功", "pinyin": "chénggōng", "meaning": "thành công"},
     ]},
]

# HSK 3 Topics (intermediate)
HSK3_LESSONS = [
    {"title": "Bài 7: Môi trường làm việc", "description": "Từ vựng về công sở", "estimated_time": 14,
     "vocabularies": [
         {"word": "办公室", "pinyin": "bàngōngshì", "meaning": "văn phòng"},
         {"word": "同事", "pinyin": "tóngshì", "meaning": "đồng nghiệp"},
         {"word": "老板", "pinyin": "lǎobǎn", "meaning": "sếp"},
         {"word": "会议", "pinyin": "huìyì", "meaning": "cuộc họp"},
         {"word": "报告", "pinyin": "bàogào", "meaning": "báo cáo"},
         {"word": "加班", "pinyin": "jiābān", "meaning": "làm thêm"},
         {"word": "工资", "pinyin": "gōngzī", "meaning": "lương"},
         {"word": "请假", "pinyin": "qǐngjià", "meaning": "xin nghỉ phép"},
     ]},
    {"title": "Bài 8: Giáo dục", "description": "Nói về học tập và trường học", "estimated_time": 14,
     "vocabularies": [
         {"word": "大学", "pinyin": "dàxué", "meaning": "đại học"},
         {"word": "专业", "pinyin": "zhuānyè", "meaning": "chuyên ngành"},
         {"word": "毕业", "pinyin": "bìyè", "meaning": "tốt nghiệp"},
         {"word": "考试", "pinyin": "kǎoshì", "meaning": "thi"},
         {"word": "成绩", "pinyin": "chéngjì", "meaning": "thành tích"},
         {"word": "课程", "pinyin": "kèchéng", "meaning": "khóa học"},
         {"word": "教授", "pinyin": "jiàoshòu", "meaning": "giáo sư"},
         {"word": "研究", "pinyin": "yánjiū", "meaning": "nghiên cứu"},
     ]},
    {"title": "Bài 9: Văn hóa Trung Hoa", "description": "Học về văn hóa truyền thống", "estimated_time": 14,
     "vocabularies": [
         {"word": "传统", "pinyin": "chuántǒng", "meaning": "truyền thống"},
         {"word": "节日", "pinyin": "jiérì", "meaning": "lễ hội"},
         {"word": "春节", "pinyin": "chūnjié", "meaning": "Tết Nguyên Đán"},
         {"word": "中秋节", "pinyin": "zhōngqiūjié", "meaning": "Tết Trung Thu"},
         {"word": "习俗", "pinyin": "xísú", "meaning": "phong tục"},
         {"word": "红包", "pinyin": "hóngbāo", "meaning": "bao lì xì"},
         {"word": "饺子", "pinyin": "jiǎozi", "meaning": "sủi cảo"},
         {"word": "龙", "pinyin": "lóng", "meaning": "rồng"},
     ]},
    {"title": "Bài 10: Công nghệ", "description": "Từ vựng về internet và điện thoại", "estimated_time": 14,
     "vocabularies": [
         {"word": "手机", "pinyin": "shǒujī", "meaning": "điện thoại"},
         {"word": "电脑", "pinyin": "diànnǎo", "meaning": "máy tính"},
         {"word": "网站", "pinyin": "wǎngzhàn", "meaning": "website"},
         {"word": "软件", "pinyin": "ruǎnjiàn", "meaning": "phần mềm"},
         {"word": "下载", "pinyin": "xiàzǎi", "meaning": "tải xuống"},
         {"word": "密码", "pinyin": "mìmǎ", "meaning": "mật khẩu"},
         {"word": "账号", "pinyin": "zhànghào", "meaning": "tài khoản"},
         {"word": "视频", "pinyin": "shìpín", "meaning": "video"},
     ]},
    {"title": "Bài 11: Du lịch nước ngoài", "description": "Chuẩn bị cho chuyến đi", "estimated_time": 14,
     "vocabularies": [
         {"word": "护照", "pinyin": "hùzhào", "meaning": "hộ chiếu"},
         {"word": "签证", "pinyin": "qiānzhèng", "meaning": "visa"},
         {"word": "机票", "pinyin": "jīpiào", "meaning": "vé máy bay"},
         {"word": "行李", "pinyin": "xíngli", "meaning": "hành lý"},
         {"word": "海关", "pinyin": "hǎiguān", "meaning": "hải quan"},
         {"word": "导游", "pinyin": "dǎoyóu", "meaning": "hướng dẫn viên"},
         {"word": "景点", "pinyin": "jǐngdiǎn", "meaning": "điểm tham quan"},
         {"word": "纪念品", "pinyin": "jìniànpǐn", "meaning": "quà lưu niệm"},
     ]},
    {"title": "Bài 12: Mối quan hệ xã hội", "description": "Giao tiếp xã hội và kết bạn", "estimated_time": 14,
     "vocabularies": [
         {"word": "朋友", "pinyin": "péngyou", "meaning": "bạn bè"},
         {"word": "邻居", "pinyin": "línjū", "meaning": "hàng xóm"},
         {"word": "约会", "pinyin": "yuēhuì", "meaning": "hẹn hò"},
         {"word": "聚会", "pinyin": "jùhuì", "meaning": "tụ họp"},
         {"word": "介绍", "pinyin": "jièshào", "meaning": "giới thiệu"},
         {"word": "联系", "pinyin": "liánxì", "meaning": "liên lạc"},
         {"word": "信任", "pinyin": "xìnrèn", "meaning": "tin tưởng"},
         {"word": "帮助", "pinyin": "bāngzhù", "meaning": "giúp đỡ"},
     ]},
    {"title": "Bài 13: Tin tức và truyền thông", "description": "Đọc và thảo luận tin tức", "estimated_time": 14,
     "vocabularies": [
         {"word": "新闻", "pinyin": "xīnwén", "meaning": "tin tức"},
         {"word": "报纸", "pinyin": "bàozhǐ", "meaning": "báo"},
         {"word": "杂志", "pinyin": "zázhì", "meaning": "tạp chí"},
         {"word": "记者", "pinyin": "jìzhě", "meaning": "nhà báo"},
         {"word": "采访", "pinyin": "cǎifǎng", "meaning": "phỏng vấn"},
         {"word": "广告", "pinyin": "guǎnggào", "meaning": "quảng cáo"},
         {"word": "社交媒体", "pinyin": "shèjiāo méitǐ", "meaning": "mạng xã hội"},
         {"word": "消息", "pinyin": "xiāoxi", "meaning": "thông tin"},
     ]},
    {"title": "Bài 14: Bảo vệ môi trường", "description": "Ý thức bảo vệ môi trường", "estimated_time": 14,
     "vocabularies": [
         {"word": "环境", "pinyin": "huánjìng", "meaning": "môi trường"},
         {"word": "污染", "pinyin": "wūrǎn", "meaning": "ô nhiễm"},
         {"word": "垃圾", "pinyin": "lājī", "meaning": "rác"},
         {"word": "回收", "pinyin": "huíshōu", "meaning": "tái chế"},
         {"word": "节约", "pinyin": "jiéyuē", "meaning": "tiết kiệm"},
         {"word": "保护", "pinyin": "bǎohù", "meaning": "bảo vệ"},
         {"word": "能源", "pinyin": "néngyuán", "meaning": "năng lượng"},
         {"word": "绿色", "pinyin": "lǜsè", "meaning": "xanh/thân thiện"},
     ]},
]

# HSK 4 Topics (upper intermediate)
HSK4_LESSONS = [
    {"title": "Bài 7: Kinh tế và tài chính", "description": "Từ vựng về tiền bạc và đầu tư", "estimated_time": 15,
     "vocabularies": [
         {"word": "经济", "pinyin": "jīngjì", "meaning": "kinh tế"},
         {"word": "投资", "pinyin": "tóuzī", "meaning": "đầu tư"},
         {"word": "股票", "pinyin": "gǔpiào", "meaning": "cổ phiếu"},
         {"word": "银行", "pinyin": "yínháng", "meaning": "ngân hàng"},
         {"word": "贷款", "pinyin": "dàikuǎn", "meaning": "vay"},
         {"word": "利息", "pinyin": "lìxī", "meaning": "lãi suất"},
         {"word": "存款", "pinyin": "cúnkuǎn", "meaning": "tiền gửi"},
         {"word": "汇率", "pinyin": "huìlǜ", "meaning": "tỷ giá"},
     ]},
    {"title": "Bài 8: Pháp luật", "description": "Hiểu biết về luật pháp cơ bản", "estimated_time": 15,
     "vocabularies": [
         {"word": "法律", "pinyin": "fǎlǜ", "meaning": "pháp luật"},
         {"word": "合同", "pinyin": "hétong", "meaning": "hợp đồng"},
         {"word": "权利", "pinyin": "quánlì", "meaning": "quyền lợi"},
         {"word": "义务", "pinyin": "yìwù", "meaning": "nghĩa vụ"},
         {"word": "规定", "pinyin": "guīdìng", "meaning": "quy định"},
         {"word": "违法", "pinyin": "wéifǎ", "meaning": "vi phạm"},
         {"word": "律师", "pinyin": "lǜshī", "meaning": "luật sư"},
         {"word": "证据", "pinyin": "zhèngjù", "meaning": "bằng chứng"},
     ]},
    {"title": "Bài 9: Chính trị và xã hội", "description": "Từ vựng về chính trị", "estimated_time": 15,
     "vocabularies": [
         {"word": "政府", "pinyin": "zhèngfǔ", "meaning": "chính phủ"},
         {"word": "政策", "pinyin": "zhèngcè", "meaning": "chính sách"},
         {"word": "公民", "pinyin": "gōngmín", "meaning": "công dân"},
         {"word": "选举", "pinyin": "xuǎnjǔ", "meaning": "bầu cử"},
         {"word": "民主", "pinyin": "mínzhǔ", "meaning": "dân chủ"},
         {"word": "国际", "pinyin": "guójì", "meaning": "quốc tế"},
         {"word": "和平", "pinyin": "hépíng", "meaning": "hòa bình"},
         {"word": "发展", "pinyin": "fāzhǎn", "meaning": "phát triển"},
     ]},
    {"title": "Bài 10: Y học và sức khỏe", "description": "Từ vựng y tế nâng cao", "estimated_time": 15,
     "vocabularies": [
         {"word": "治疗", "pinyin": "zhìliáo", "meaning": "điều trị"},
         {"word": "手术", "pinyin": "shǒushù", "meaning": "phẫu thuật"},
         {"word": "检查", "pinyin": "jiǎnchá", "meaning": "kiểm tra"},
         {"word": "诊断", "pinyin": "zhěnduàn", "meaning": "chẩn đoán"},
         {"word": "症状", "pinyin": "zhèngzhuàng", "meaning": "triệu chứng"},
         {"word": "疫苗", "pinyin": "yìmiáo", "meaning": "vaccine"},
         {"word": "康复", "pinyin": "kāngfù", "meaning": "phục hồi"},
         {"word": "预防", "pinyin": "yùfáng", "meaning": "phòng ngừa"},
     ]},
    {"title": "Bài 11: Nghệ thuật và văn học", "description": "Thưởng thức nghệ thuật", "estimated_time": 15,
     "vocabularies": [
         {"word": "艺术", "pinyin": "yìshù", "meaning": "nghệ thuật"},
         {"word": "文学", "pinyin": "wénxué", "meaning": "văn học"},
         {"word": "作者", "pinyin": "zuòzhě", "meaning": "tác giả"},
         {"word": "小说", "pinyin": "xiǎoshuō", "meaning": "tiểu thuyết"},
         {"word": "诗歌", "pinyin": "shīgē", "meaning": "thơ ca"},
         {"word": "画家", "pinyin": "huàjiā", "meaning": "họa sĩ"},
         {"word": "博物馆", "pinyin": "bówùguǎn", "meaning": "bảo tàng"},
         {"word": "展览", "pinyin": "zhǎnlǎn", "meaning": "triển lãm"},
     ]},
    {"title": "Bài 12: Khoa học công nghệ", "description": "Phát triển công nghệ hiện đại", "estimated_time": 15,
     "vocabularies": [
         {"word": "科学", "pinyin": "kēxué", "meaning": "khoa học"},
         {"word": "技术", "pinyin": "jìshù", "meaning": "công nghệ"},
         {"word": "发明", "pinyin": "fāmíng", "meaning": "phát minh"},
         {"word": "实验", "pinyin": "shíyàn", "meaning": "thí nghiệm"},
         {"word": "数据", "pinyin": "shùjù", "meaning": "dữ liệu"},
         {"word": "人工智能", "pinyin": "réngōng zhìnéng", "meaning": "AI"},
         {"word": "机器人", "pinyin": "jīqìrén", "meaning": "robot"},
         {"word": "创新", "pinyin": "chuàngxīn", "meaning": "sáng tạo"},
     ]},
    {"title": "Bài 13: Triết học và tư tưởng", "description": "Tư tưởng và triết lý sống", "estimated_time": 15,
     "vocabularies": [
         {"word": "哲学", "pinyin": "zhéxué", "meaning": "triết học"},
         {"word": "思想", "pinyin": "sīxiǎng", "meaning": "tư tưởng"},
         {"word": "道德", "pinyin": "dàodé", "meaning": "đạo đức"},
         {"word": "价值", "pinyin": "jiàzhí", "meaning": "giá trị"},
         {"word": "信仰", "pinyin": "xìnyǎng", "meaning": "tín ngưỡng"},
         {"word": "精神", "pinyin": "jīngshén", "meaning": "tinh thần"},
         {"word": "智慧", "pinyin": "zhìhuì", "meaning": "trí tuệ"},
         {"word": "修养", "pinyin": "xiūyǎng", "meaning": "tu dưỡng"},
     ]},
    {"title": "Bài 14: Quan hệ quốc tế", "description": "Ngoại giao và hợp tác quốc tế", "estimated_time": 15,
     "vocabularies": [
         {"word": "外交", "pinyin": "wàijiāo", "meaning": "ngoại giao"},
         {"word": "大使馆", "pinyin": "dàshǐguǎn", "meaning": "đại sứ quán"},
         {"word": "合作", "pinyin": "hézuò", "meaning": "hợp tác"},
         {"word": "谈判", "pinyin": "tánpàn", "meaning": "đàm phán"},
         {"word": "协议", "pinyin": "xiéyì", "meaning": "hiệp định"},
         {"word": "贸易", "pinyin": "màoyì", "meaning": "thương mại"},
         {"word": "文化交流", "pinyin": "wénhuà jiāoliú", "meaning": "giao lưu văn hóa"},
         {"word": "全球化", "pinyin": "quánqiúhuà", "meaning": "toàn cầu hóa"},
     ]},
]

# HSK 5 Topics (advanced)
HSK5_LESSONS = [
    {"title": "Bài 1: Tâm lý học cơ bản", "description": "Hiểu về tâm lý con người", "estimated_time": 18,
     "vocabularies": [
         {"word": "心理", "pinyin": "xīnlǐ", "meaning": "tâm lý"},
         {"word": "情绪", "pinyin": "qíngxù", "meaning": "cảm xúc"},
         {"word": "压力", "pinyin": "yālì", "meaning": "áp lực"},
         {"word": "焦虑", "pinyin": "jiāolǜ", "meaning": "lo âu"},
         {"word": "心态", "pinyin": "xīntài", "meaning": "tâm thái"},
         {"word": "性格", "pinyin": "xìnggé", "meaning": "tính cách"},
         {"word": "动机", "pinyin": "dòngjī", "meaning": "động cơ"},
         {"word": "潜意识", "pinyin": "qiányìshí", "meaning": "tiềm thức"},
     ]},
    {"title": "Bài 2: Lịch sử Trung Quốc", "description": "Các triều đại và sự kiện quan trọng", "estimated_time": 18,
     "vocabularies": [
         {"word": "历史", "pinyin": "lìshǐ", "meaning": "lịch sử"},
         {"word": "朝代", "pinyin": "cháodài", "meaning": "triều đại"},
         {"word": "皇帝", "pinyin": "huángdì", "meaning": "hoàng đế"},
         {"word": "战争", "pinyin": "zhànzhēng", "meaning": "chiến tranh"},
         {"word": "革命", "pinyin": "gémìng", "meaning": "cách mạng"},
         {"word": "文明", "pinyin": "wénmíng", "meaning": "văn minh"},
         {"word": "遗产", "pinyin": "yíchǎn", "meaning": "di sản"},
         {"word": "考古", "pinyin": "kǎogǔ", "meaning": "khảo cổ"},
     ]},
    {"title": "Bài 3: Kinh doanh quốc tế", "description": "Từ vựng kinh doanh nâng cao", "estimated_time": 18,
     "vocabularies": [
         {"word": "企业", "pinyin": "qǐyè", "meaning": "doanh nghiệp"},
         {"word": "市场", "pinyin": "shìchǎng", "meaning": "thị trường"},
         {"word": "竞争", "pinyin": "jìngzhēng", "meaning": "cạnh tranh"},
         {"word": "战略", "pinyin": "zhànlüè", "meaning": "chiến lược"},
         {"word": "利润", "pinyin": "lìrùn", "meaning": "lợi nhuận"},
         {"word": "风险", "pinyin": "fēngxiǎn", "meaning": "rủi ro"},
         {"word": "品牌", "pinyin": "pǐnpái", "meaning": "thương hiệu"},
         {"word": "营销", "pinyin": "yíngxiāo", "meaning": "marketing"},
     ]},
    {"title": "Bài 4: Văn học cổ điển", "description": "Tác phẩm văn học Trung Hoa", "estimated_time": 18,
     "vocabularies": [
         {"word": "古典", "pinyin": "gǔdiǎn", "meaning": "cổ điển"},
         {"word": "名著", "pinyin": "míngzhù", "meaning": "tác phẩm nổi tiếng"},
         {"word": "典故", "pinyin": "diǎngù", "meaning": "điển tích"},
         {"word": "成语", "pinyin": "chéngyǔ", "meaning": "thành ngữ"},
         {"word": "寓言", "pinyin": "yùyán", "meaning": "ngụ ngôn"},
         {"word": "传说", "pinyin": "chuánshuō", "meaning": "truyền thuyết"},
         {"word": "神话", "pinyin": "shénhuà", "meaning": "thần thoại"},
         {"word": "散文", "pinyin": "sǎnwén", "meaning": "tản văn"},
     ]},
    {"title": "Bài 5: Khoa học xã hội", "description": "Nghiên cứu xã hội học", "estimated_time": 18,
     "vocabularies": [
         {"word": "社会", "pinyin": "shèhuì", "meaning": "xã hội"},
         {"word": "阶层", "pinyin": "jiēcéng", "meaning": "giai tầng"},
         {"word": "群体", "pinyin": "qúntǐ", "meaning": "nhóm"},
         {"word": "文化", "pinyin": "wénhuà", "meaning": "văn hóa"},
         {"word": "现象", "pinyin": "xiànxiàng", "meaning": "hiện tượng"},
         {"word": "调查", "pinyin": "diàochá", "meaning": "điều tra"},
         {"word": "统计", "pinyin": "tǒngjì", "meaning": "thống kê"},
         {"word": "分析", "pinyin": "fēnxī", "meaning": "phân tích"},
     ]},
    {"title": "Bài 6: Y học cổ truyền", "description": "Đông y và thiền định", "estimated_time": 18,
     "vocabularies": [
         {"word": "中医", "pinyin": "zhōngyī", "meaning": "đông y"},
         {"word": "针灸", "pinyin": "zhēnjiǔ", "meaning": "châm cứu"},
         {"word": "草药", "pinyin": "cǎoyào", "meaning": "thảo dược"},
         {"word": "穴位", "pinyin": "xuéwèi", "meaning": "huyệt đạo"},
         {"word": "气功", "pinyin": "qìgōng", "meaning": "khí công"},
         {"word": "太极", "pinyin": "tàijí", "meaning": "thái cực"},
         {"word": "养生", "pinyin": "yǎngshēng", "meaning": "dưỡng sinh"},
         {"word": "阴阳", "pinyin": "yīnyáng", "meaning": "âm dương"},
     ]},
    {"title": "Bài 7: Môi trường và sinh thái", "description": "Biến đổi khí hậu và bảo tồn", "estimated_time": 18,
     "vocabularies": [
         {"word": "生态", "pinyin": "shēngtài", "meaning": "sinh thái"},
         {"word": "气候", "pinyin": "qìhòu", "meaning": "khí hậu"},
         {"word": "变化", "pinyin": "biànhuà", "meaning": "biến đổi"},
         {"word": "温室效应", "pinyin": "wēnshì xiàoyìng", "meaning": "hiệu ứng nhà kính"},
         {"word": "物种", "pinyin": "wùzhǒng", "meaning": "loài"},
         {"word": "灭绝", "pinyin": "mièjué", "meaning": "tuyệt chủng"},
         {"word": "可持续", "pinyin": "kě chíxù", "meaning": "bền vững"},
         {"word": "碳排放", "pinyin": "tàn páifàng", "meaning": "khí thải carbon"},
     ]},
    {"title": "Bài 8: Triết học Đông phương", "description": "Khổng Tử, Lão Tử và các trường phái", "estimated_time": 18,
     "vocabularies": [
         {"word": "儒家", "pinyin": "rújiā", "meaning": "Nho gia"},
         {"word": "道家", "pinyin": "dàojiā", "meaning": "Đạo gia"},
         {"word": "佛家", "pinyin": "fójiā", "meaning": "Phật gia"},
         {"word": "圣人", "pinyin": "shèngrén", "meaning": "thánh nhân"},
         {"word": "仁义", "pinyin": "rényì", "meaning": "nhân nghĩa"},
         {"word": "自然", "pinyin": "zìrán", "meaning": "tự nhiên"},
         {"word": "修行", "pinyin": "xiūxíng", "meaning": "tu hành"},
         {"word": "悟道", "pinyin": "wùdào", "meaning": "ngộ đạo"},
     ]},
    {"title": "Bài 9: Nghệ thuật biểu diễn", "description": "Kinh kịch và nghệ thuật truyền thống", "estimated_time": 18,
     "vocabularies": [
         {"word": "京剧", "pinyin": "jīngjù", "meaning": "kinh kịch"},
         {"word": "表演", "pinyin": "biǎoyǎn", "meaning": "biểu diễn"},
         {"word": "舞台", "pinyin": "wǔtái", "meaning": "sân khấu"},
         {"word": "演员", "pinyin": "yǎnyuán", "meaning": "diễn viên"},
         {"word": "角色", "pinyin": "juésè", "meaning": "vai diễn"},
         {"word": "服装", "pinyin": "fúzhuāng", "meaning": "trang phục"},
         {"word": "脸谱", "pinyin": "liǎnpǔ", "meaning": "mặt nạ"},
         {"word": "传承", "pinyin": "chuánchéng", "meaning": "truyền thừa"},
     ]},
    {"title": "Bài 10: Kiến trúc Trung Hoa", "description": "Phong cách kiến trúc truyền thống", "estimated_time": 18,
     "vocabularies": [
         {"word": "建筑", "pinyin": "jiànzhù", "meaning": "kiến trúc"},
         {"word": "宫殿", "pinyin": "gōngdiàn", "meaning": "cung điện"},
         {"word": "庙宇", "pinyin": "miàoyǔ", "meaning": "đền chùa"},
         {"word": "园林", "pinyin": "yuánlín", "meaning": "vườn cảnh"},
         {"word": "风水", "pinyin": "fēngshuǐ", "meaning": "phong thủy"},
         {"word": "雕刻", "pinyin": "diāokè", "meaning": "điêu khắc"},
         {"word": "屋顶", "pinyin": "wūdǐng", "meaning": "mái nhà"},
         {"word": "石狮", "pinyin": "shíshī", "meaning": "sư tử đá"},
     ]},
    {"title": "Bài 11: Thư pháp và hội họa", "description": "Nghệ thuật viết và vẽ", "estimated_time": 18,
     "vocabularies": [
         {"word": "书法", "pinyin": "shūfǎ", "meaning": "thư pháp"},
         {"word": "毛笔", "pinyin": "máobǐ", "meaning": "bút lông"},
         {"word": "墨水", "pinyin": "mòshuǐ", "meaning": "mực"},
         {"word": "宣纸", "pinyin": "xuānzhǐ", "meaning": "giấy tuyên"},
         {"word": "笔画", "pinyin": "bǐhuà", "meaning": "nét chữ"},
         {"word": "山水画", "pinyin": "shānshuǐ huà", "meaning": "tranh sơn thủy"},
         {"word": "水墨", "pinyin": "shuǐmò", "meaning": "thủy mặc"},
         {"word": "临摹", "pinyin": "línmó", "meaning": "sao chép"},
     ]},
    {"title": "Bài 12: Âm nhạc Trung Hoa", "description": "Nhạc cụ và âm nhạc truyền thống", "estimated_time": 18,
     "vocabularies": [
         {"word": "乐器", "pinyin": "yuèqì", "meaning": "nhạc cụ"},
         {"word": "古筝", "pinyin": "gǔzhēng", "meaning": "đàn tranh"},
         {"word": "二胡", "pinyin": "èrhú", "meaning": "đàn nhị"},
         {"word": "琵琶", "pinyin": "pípá", "meaning": "đàn tỳ bà"},
         {"word": "笛子", "pinyin": "dízi", "meaning": "sáo"},
         {"word": "旋律", "pinyin": "xuánlǜ", "meaning": "giai điệu"},
         {"word": "民歌", "pinyin": "míngē", "meaning": "dân ca"},
         {"word": "戏曲", "pinyin": "xìqǔ", "meaning": "hí khúc"},
     ]},
    {"title": "Bài 13: Ẩm thực Trung Hoa", "description": "Văn hóa ẩm thực và các trường phái", "estimated_time": 18,
     "vocabularies": [
         {"word": "烹饪", "pinyin": "pēngrèn", "meaning": "nấu nướng"},
         {"word": "菜系", "pinyin": "càixì", "meaning": "hệ thống ẩm thực"},
         {"word": "食材", "pinyin": "shícái", "meaning": "nguyên liệu"},
         {"word": "调料", "pinyin": "tiáoliào", "meaning": "gia vị"},
         {"word": "刀工", "pinyin": "dāogōng", "meaning": "kỹ thuật dao"},
         {"word": "火候", "pinyin": "huǒhòu", "meaning": "độ lửa"},
         {"word": "宴席", "pinyin": "yànxí", "meaning": "tiệc"},
         {"word": "品尝", "pinyin": "pǐncháng", "meaning": "thưởng thức"},
     ]},
    {"title": "Bài 14: Trà đạo Trung Hoa", "description": "Văn hóa và nghệ thuật thưởng trà", "estimated_time": 18,
     "vocabularies": [
         {"word": "茶道", "pinyin": "chádào", "meaning": "trà đạo"},
         {"word": "茶叶", "pinyin": "cháyè", "meaning": "lá trà"},
         {"word": "茶具", "pinyin": "chájù", "meaning": "dụng cụ pha trà"},
         {"word": "泡茶", "pinyin": "pàochá", "meaning": "pha trà"},
         {"word": "茶壶", "pinyin": "cháhú", "meaning": "ấm trà"},
         {"word": "茶杯", "pinyin": "chábēi", "meaning": "tách trà"},
         {"word": "绿茶", "pinyin": "lǜchá", "meaning": "trà xanh"},
         {"word": "红茶", "pinyin": "hóngchá", "meaning": "trà đen"},
     ]},
]


def seed_all_hsk_lessons():
    db = SessionLocal()
    
    try:
        all_data = [
            (2, HSK2_LESSONS),
            (3, HSK3_LESSONS),
            (4, HSK4_LESSONS),
            (5, HSK5_LESSONS),
        ]
        
        for hsk_level, lessons_data in all_data:
            print(f"\n📚 Processing HSK {hsk_level}...")
            
            # Get current lesson count
            current_count = db.query(Lesson).filter(Lesson.hsk_level == hsk_level).count()
            print(f"   Current lessons: {current_count}")
            
            created_count = 0
            
            for i, lesson_data in enumerate(lessons_data):
                # Check if lesson already exists
                exists = db.query(Lesson).filter(
                    Lesson.title == lesson_data["title"],
                    Lesson.hsk_level == hsk_level
                ).first()
                
                if exists:
                    print(f"   ⏭️  Skipping: {lesson_data['title']} (already exists)")
                    continue
                
                # Create lesson
                order = current_count + i + 1
                lesson = Lesson(
                    title=lesson_data["title"],
                    description=lesson_data["description"],
                    hsk_level=hsk_level,
                    order=order,
                    estimated_time=lesson_data["estimated_time"],
                    is_published=True
                )
                db.add(lesson)
                db.flush()
                
                # Add vocabularies
                for vocab_data in lesson_data.get("vocabularies", []):
                    vocab = db.query(Vocabulary).filter(
                        Vocabulary.word == vocab_data["word"]
                    ).first()
                    
                    if not vocab:
                        vocab = Vocabulary(
                            word=vocab_data["word"],
                            pinyin=vocab_data["pinyin"],
                            meaning=vocab_data["meaning"],
                            hsk_level=hsk_level
                        )
                        db.add(vocab)
                        db.flush()
                    
                    lesson.vocabularies.append(vocab)
                
                # Create default units
                default_units = [
                    {"type": "vocabulary", "title": "Học từ vựng", "order": 1, "duration_minutes": 5},
                    {"type": "listening", "title": "Nghe hiểu", "order": 2, "duration_minutes": 5},
                    {"type": "speaking", "title": "Luyện nói", "order": 3, "duration_minutes": 5},
                    {"type": "exercise", "title": "Bài tập", "order": 4, "duration_minutes": 5},
                ]
                
                for unit_data in default_units:
                    unit = Unit(
                        lesson_id=lesson.id,
                        type=unit_data["type"],
                        title=unit_data["title"],
                        order=unit_data["order"],
                        duration_minutes=unit_data["duration_minutes"]
                    )
                    db.add(unit)
                
                print(f"   ✅ Created: {lesson_data['title']} ({len(lesson_data.get('vocabularies', []))} words)")
                created_count += 1
            
            print(f"   📝 Created {created_count} new lessons for HSK {hsk_level}")
        
        db.commit()
        
        # Final summary
        print("\n" + "="*50)
        print("🎉 FINAL SUMMARY:")
        for level in range(1, 6):
            count = db.query(Lesson).filter(Lesson.hsk_level == level).count()
            print(f"   HSK {level}: {count} lessons")
        print("="*50)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_all_hsk_lessons()
