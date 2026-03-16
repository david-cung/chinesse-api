from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta

from database.database import get_db
from models.quiz import QuizAttempt, WordStats
from models.review import ReviewCard
from models.progress import UserProgress, UserItemProgress, Achievement, UserAchievement
from models.lesson import Lesson
from schemas import schemas
from utils.dependencies import get_current_user
from models.user import User

router = APIRouter(
    prefix="/api/v1/stats",
    tags=["stats"]
)

@router.get("/overview", response_model=schemas.StatsOverviewResponse)
def get_stats_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get weekly overview stats"""
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # New words today (based on UserItemProgress or similar)
    # For now, mock or use basic count
    new_words_today = 0 # Need to implement in progress tracking
    
    # Reviewed today
    reviewed_today = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id,
        QuizAttempt.created_at >= today
    ).count()
    
    # Accuracy
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id,
        QuizAttempt.created_at >= today - timedelta(days=7)
    ).all()
    
    total_q = sum(a.total_questions for a in attempts) if attempts else 0
    total_c = sum(a.correct_answers for a in attempts) if attempts else 0
    accuracy = (total_c / total_q * 100) if total_q > 0 else 0
    
    return {
        "new_words_today": new_words_today,
        "reviewed_today": reviewed_today,
        "accuracy_percent": accuracy,
        "current_streak": current_user.streak
    }

@router.get("/timeline", response_model=schemas.StatsTimelineResponse)
def get_stats_timeline(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get daily right/wrong counts for the timeline chart"""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Group by date
    results = db.query(
        func.date(QuizAttempt.created_at).label("day"),
        func.sum(QuizAttempt.correct_answers).label("right"),
        func.sum(QuizAttempt.total_questions - QuizAttempt.correct_answers).label("wrong")
    ).filter(
        QuizAttempt.user_id == current_user.id,
        QuizAttempt.created_at >= start_date
    ).group_by(func.date(QuizAttempt.created_at)).all()
    
    timeline = []
    # Fill in gaps with 0
    date_map = {str(r.day): r for r in results}
    for i in range(days):
        d = (start_date + timedelta(days=i)).date()
        d_str = str(d)
        if d_str in date_map:
            r = date_map[d_str]
            timeline.append({
                "date": d_str,
                "right_count": int(r.right),
                "wrong_count": int(r.wrong)
            })
        else:
            timeline.append({
                "date": d_str,
                "right_count": 0,
                "wrong_count": 0
            })
            
    return {"timeline": timeline}


@router.get("/current-goal", response_model=schemas.CurrentGoalProgressResponse)
def get_current_goal_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lấy tiến độ lộ trình HSK hiện tại của User"""
    
    # Tìm HSK level gần nhất user đang học
    recent_progress = db.query(UserProgress).join(Lesson).filter(
        UserProgress.user_id == current_user.id
    ).order_by(UserProgress.last_accessed_at.desc()).first()
    
    current_hsk_level = recent_progress.lesson.hsk_level if recent_progress and recent_progress.lesson else 1
    
    # Lấy tổng số bài học (Lesson) của HSK level này
    total_lessons = db.query(Lesson).filter(
        Lesson.hsk_level == current_hsk_level,
        Lesson.is_published == True
    ).count()
    
    if total_lessons == 0:
        return {"current_level": f"HSK {current_hsk_level}", "progress_percent": 0.0}
    
    # Tính số bài đã completed
    completed_lessons = db.query(UserProgress).join(Lesson).filter(
        UserProgress.user_id == current_user.id,
        Lesson.hsk_level == current_hsk_level,
        UserProgress.completed == True
    ).count()
    
    # Tính tỷ lệ hoàn thành trung bình của các bài đang học dở
    in_progress_lessons = db.query(UserProgress).join(Lesson).filter(
        UserProgress.user_id == current_user.id,
        Lesson.hsk_level == current_hsk_level,
        UserProgress.completed == False
    ).all()
    
    partial_progress = sum((p.progress_percent or 0) / 100.0 for p in in_progress_lessons)
    
    total_progress_score = completed_lessons + partial_progress
    progress_percent = (total_progress_score / total_lessons) * 100
    
    return {
        "current_level": f"HSK {current_hsk_level}",
        "progress_percent": round(progress_percent, 1)
    }


@router.get("/weekly-time", response_model=schemas.WeeklyStudyTimeResponse)
def get_weekly_study_time(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lấy thời gian học trong 7 ngày gần nhất.
    Hiện tại mock từ QuizAttempt (1 quiz attempt = 5 phút)
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=6) # 7 ngày tính cả hôm nay
    
    # Lấy quiz của tuần này
    this_week_attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id,
        QuizAttempt.created_at >= start_date
    ).all()
    
    # Lấy quiz của tuần trước để so sánh
    last_week_start = start_date - timedelta(days=7)
    last_week_attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id,
        QuizAttempt.created_at >= last_week_start,
        QuizAttempt.created_at < start_date
    ).all()
    
    # Gom nhóm theo ngày cho tuần này
    daily_time = { (start_date + timedelta(days=i)).date(): 0 for i in range(7) }
    
    # Giả lập: mỗi bài quiz = 5 phút học (hoặc lấy time_spent_seconds nếu có)
    # Trong mô hình của ta, QuizAttemptCreateSchema có time_spent_seconds nhưng DB model chưa thấy, ta sẽ giả định 1 attempt = 5 phút = 300s
    for attempt in this_week_attempts:
        d = attempt.created_at.date()
        if d in daily_time:
            # 5 phút / 60 phút = giờ
            daily_time[d] += (5 / 60)
            
    # Tính tổng giờ tuần này và tuần trước
    total_hours_this_week = sum(daily_time.values())
    total_hours_last_week = len(last_week_attempts) * (5 / 60)
    
    # Tính % thay đổi
    if total_hours_last_week == 0:
        change_percent = 100.0 if total_hours_this_week > 0 else 0.0
    else:
        change_percent = ((total_hours_this_week - total_hours_last_week) / total_hours_last_week) * 100
        
    days_vn = ["CN", "T2", "T3", "T4", "T5", "T6", "T7"]
    
    daily_stats = []
    for d, hours in daily_time.items():
        # d.weekday() trả về 0(Thứ 2) -> 6(CN)
        # Trong hệ thống VN thường gọi T2, T3...
        day_index = (d.weekday() + 1) % 7
        daily_stats.append({
            "day": days_vn[day_index],
            "hours": round(hours, 2)
        })
        
    return {
        "total_hours_this_week": round(total_hours_this_week, 2),
        "change_percent": round(change_percent, 1),
        "daily_stats": daily_stats
    }


@router.get("/vocabulary-growth", response_model=schemas.VocabGrowthResponse)
def get_vocabulary_growth(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Đếm số từ vựng mới học tuần này so với tuần trước"""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    last_week_start = start_date - timedelta(days=7)
    
    this_week_words = db.query(UserItemProgress).filter(
        UserItemProgress.user_id == current_user.id,
        UserItemProgress.item_type == "vocabulary",
        UserItemProgress.completed == True,
        UserItemProgress.last_accessed_at >= start_date
    ).count()
    
    last_week_words = db.query(UserItemProgress).filter(
        UserItemProgress.user_id == current_user.id,
        UserItemProgress.item_type == "vocabulary",
        UserItemProgress.completed == True,
        UserItemProgress.last_accessed_at >= last_week_start,
        UserItemProgress.last_accessed_at < start_date
    ).count()
    
    if last_week_words == 0:
        growth_percent = 100.0 if this_week_words > 0 else 0.0
    else:
        growth_percent = ((this_week_words - last_week_words) / last_week_words) * 100
        
    return {
        "new_words_this_week": this_week_words,
        "growth_percent": round(growth_percent, 1)
    }


@router.get("/achievements", response_model=List[schemas.AchievementResponse])
def get_user_achievements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lấy danh sách thành tựu.
    Tự động kiểm tra và unlock các thành tựu mới nếu đủ điều kiện.
    """
    
    # 1. Đảm bảo có danh sách cúp cơ bản trong DB (nếu chưa có thì seed luôn cho tiện test)
    if db.query(Achievement).count() == 0:
        basic_achievements = [
            Achievement(title="Chăm chỉ", description="Đạt chuỗi 3 ngày học liên tiếp", icon="flame", condition_type="streak", condition_value=3),
            Achievement(title="Lửa cháy", description="Đạt chuỗi 7 ngày học liên tiếp", icon="flame", condition_type="streak", condition_value=7),
            Achievement(title="Khởi đầu", description="Hoàn thành bài học đầu tiên", icon="book", condition_type="lesson_complete", condition_value=1),
            Achievement(title="Hoàn hảo", description="Đạt 100% điểm một bài Quiz", icon="award", condition_type="perfect_quiz", condition_value=1),
        ]
        db.add_all(basic_achievements)
        db.commit()
        
    all_achievements = db.query(Achievement).all()
    unlocked_ids = { ua.achievement_id: ua.unlocked_at for ua in db.query(UserAchievement).filter(UserAchievement.user_id == current_user.id).all() }
    
    # 2. Kiểm tra điều kiện unlock
    new_unlocks = []
    
    for ach in all_achievements:
        if ach.id in unlocked_ids:
            continue # Đã unlock
            
        unlocked = False
        
        if ach.condition_type == "streak":
            if current_user.streak >= ach.condition_value:
                unlocked = True
                
        elif ach.condition_type == "lesson_complete":
            completed_count = db.query(UserProgress).filter(
                UserProgress.user_id == current_user.id,
                UserProgress.completed == True
            ).count()
            if completed_count >= ach.condition_value:
                unlocked = True
                
        elif ach.condition_type == "perfect_quiz":
            perfect_count = db.query(QuizAttempt).filter(
                QuizAttempt.user_id == current_user.id,
                QuizAttempt.score == 100
            ).count()
            if perfect_count >= ach.condition_value:
                unlocked = True
                
        if unlocked:
            new_ua = UserAchievement(user_id=current_user.id, achievement_id=ach.id)
            db.add(new_ua)
            new_unlocks.append(ach.id)
            unlocked_ids[ach.id] = datetime.utcnow()
            
    if new_unlocks:
        db.commit()
        
    # 3. Trả về kết quả
    result = []
    for ach in all_achievements:
        result.append({
            "id": ach.id,
            "title": ach.title,
            "description": ach.description,
            "icon": ach.icon,
            "is_unlocked": ach.id in unlocked_ids,
            "unlocked_at": unlocked_ids.get(ach.id)
        })
        
    return result

