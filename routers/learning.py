from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional
from database.database import get_db
from models.user import User
from models.lesson import (
    Lesson, Vocabulary, LessonObjective, 
    GrammarPoint, GrammarExample, Exercise,
    lesson_vocabulary
)
from models.sentence import Sentence
from models.unit import Unit, UnitProgress
from models.progress import UserProgress, UserItemProgress
from schemas.schemas import (
    LearningContinueResponse, 
    CourseInfo, 
    LessonInfo, 
    ProgressInfo,
    TrackItemRequest
)
from utils.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/learning", tags=["learning"])


def get_hsk_level_name(level: int) -> str:
    """Convert HSK level number to display name"""
    return f"HSK {level}"


@router.get("/continue", response_model=LearningContinueResponse)
def get_continue_learning(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the most recent lesson the user was studying.
    
    Returns:
    - course: HSK level info (id, level name)
    - lesson: Current lesson info (id, title, description)
    - progress: Learning progress (completedPercent, lastUnitId)
    
    Logic:
    1. Find the most recently accessed lesson by user
    2. If no progress, return the first lesson of HSK 1
    """
    # Find the most recent progress record
    recent_progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.completed == False  # Only incomplete lessons
    ).order_by(desc(UserProgress.last_accessed_at)).first()
    
    if recent_progress and recent_progress.lesson:
        # User has ongoing lesson
        lesson = recent_progress.lesson
        progress_percent = recent_progress.progress_percent or 0.0
        last_unit_id = f"unit_{lesson.id}_{recent_progress.exercises_completed}"
    else:
        # Check if user has completed all started lessons
        any_progress = db.query(UserProgress).filter(
            UserProgress.user_id == current_user.id
        ).order_by(desc(UserProgress.last_accessed_at)).first()
        
        if any_progress and any_progress.lesson:
            # User completed a lesson, suggest the next one
            current_lesson = any_progress.lesson
            next_lesson = db.query(Lesson).filter(
                Lesson.hsk_level == current_lesson.hsk_level,
                Lesson.order > current_lesson.order,
                Lesson.is_published == True
            ).order_by(Lesson.order).first()
            
            if not next_lesson:
                # No more lessons in current HSK level, try next level
                next_lesson = db.query(Lesson).filter(
                    Lesson.hsk_level == current_lesson.hsk_level + 1,
                    Lesson.is_published == True
                ).order_by(Lesson.order).first()
            
            if next_lesson:
                lesson = next_lesson
                progress_percent = 0.0
                last_unit_id = None
            else:
                # All lessons completed, return the last one
                lesson = current_lesson
                progress_percent = 100.0
                last_unit_id = f"unit_{lesson.id}_completed"
        else:
            # New user - get first lesson of HSK 1
            lesson = db.query(Lesson).filter(
                Lesson.hsk_level == 1,
                Lesson.is_published == True
            ).order_by(Lesson.order).first()
            
            if not lesson:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No lessons available"
                )
            
            progress_percent = 0.0
            last_unit_id = None
    
    return LearningContinueResponse(
        course=CourseInfo(
            id=f"hsk{lesson.hsk_level}",
            level=get_hsk_level_name(lesson.hsk_level)
        ),
        lesson=LessonInfo(
            id=f"lesson_{lesson.id}",
            title=lesson.title,
            description=lesson.description
        ),
        progress=ProgressInfo(
            completedPercent=progress_percent,
            lastUnitId=last_unit_id
        )
    )


# Import thêm cho courses endpoint
from schemas.schemas import LessonItem, CourseLessonsResponse
from typing import List


def parse_course_id(course_id: str) -> int:
    """Parse course ID (e.g., 'hsk1') to HSK level number"""
    if course_id.lower().startswith("hsk"):
        try:
            return int(course_id[3:])
        except ValueError:
            pass
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Invalid course ID: {course_id}. Expected format: hsk1, hsk2, etc."
    )


def get_lesson_status(
    lesson: Lesson,
    user_progress: dict,
    previous_completed: bool
) -> tuple[str, float | None]:
    """
    Determine lesson status based on user progress.
    
    Returns: (status, progressPercent)
    - completed: User finished this lesson
    - in_progress: User started but not finished
    - locked: Previous lesson not completed
    """
    progress = user_progress.get(lesson.id)
    
    if progress:
        if progress.completed:
            return "completed", None
        else:
            return "in_progress", progress.progress_percent or 0.0
    
    # No progress record for this lesson
    if previous_completed:
        return "locked", None  # Can start but hasn't yet - treat as locked until started
    else:
        return "locked", None


@router.get("/courses/{course_id}/lessons", response_model=CourseLessonsResponse)
def get_course_lessons(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all lessons for a course with user's progress status.
    
    Path params:
    - course_id: Course identifier (e.g., "hsk1", "hsk2")
    
    Returns:
    - course: Course info
    - lessons: List of lessons with status:
        - completed: User finished this lesson
        - in_progress: User started but not finished
        - locked: Previous lesson not completed
    """
    hsk_level = parse_course_id(course_id)
    
    # Get all published lessons for this HSK level
    lessons = db.query(Lesson).filter(
        Lesson.hsk_level == hsk_level,
        Lesson.is_published == True
    ).order_by(Lesson.order).all()
    
    if not lessons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No lessons found for {course_id.upper()}"
        )
    
    # Get user's progress for all lessons in this level
    lesson_ids = [l.id for l in lessons]
    progress_records = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.lesson_id.in_(lesson_ids)
    ).all()
    
    # Create lookup dict for progress
    user_progress = {p.lesson_id: p for p in progress_records}
    
    # Build lesson items with status
    lesson_items: List[LessonItem] = []
    previous_completed = True  # First lesson is always unlocked
    
    for lesson in lessons:
        progress = user_progress.get(lesson.id)
        
        # Determine status
        if progress:
            if progress.completed:
                status_str = "completed"
                progress_percent = None
            else:
                status_str = "in_progress"
                progress_percent = progress.progress_percent or 0.0
        elif previous_completed:
            # No progress but previous is done - available but not started
            # For first lesson or next unlocked lesson
            status_str = "locked"  # Show as locked until user starts
            progress_percent = None
            # Actually, the first available lesson should be unlockable
            # Let's adjust: if it's the first lesson or previous was completed, it's available
            if lesson == lessons[0]:
                status_str = "in_progress"  # First lesson is always available
                progress_percent = 0.0
            elif previous_completed:
                status_str = "locked"  # Needs user to start it
                progress_percent = None
        else:
            status_str = "locked"
            progress_percent = None
        
        # Update previous_completed for next iteration
        if progress and progress.completed:
            previous_completed = True
        else:
            previous_completed = False
        
        # Count vocabulary
        vocab_count = len(lesson.vocabularies) if lesson.vocabularies else 0
        
        lesson_items.append(LessonItem(
            id=f"lesson_{lesson.id}",
            title=lesson.title,
            vocabCount=vocab_count,
            durationMinutes=lesson.estimated_time or 10,
            status=status_str,
            progressPercent=progress_percent
        ))
    
    return CourseLessonsResponse(
        course=CourseInfo(
            id=course_id.lower(),
            level=get_hsk_level_name(hsk_level)
        ),
        lessons=lesson_items
    )


# ==================== Resume Learning Endpoint ====================
from schemas.schemas import (
    LearningResumeResponse,
    ResumeUnitInfo,
    ResumeProgressInfo,
    ResumeNavigationInfo
)
from models.unit import UNIT_TYPE_SCREENS


@router.get("/resume", response_model=LearningResumeResponse)
def get_learning_resume(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the lesson and unit a user should resume learning from.
    
    Priority rules:
    1. Find lesson with status = "in_progress"
    2. If none, return first lesson not started
    3. If all lessons completed, return last lesson
    
    Inside a lesson:
    - Find first unit with status != "completed", ordered by unit.order
    
    Returns: course, lesson, unit, progress, navigation
    """
    
    # Step 1: Find lesson with in_progress status
    in_progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.completed == False,
        UserProgress.progress_percent > 0
    ).order_by(desc(UserProgress.last_accessed_at)).first()
    
    if in_progress and in_progress.lesson:
        lesson = in_progress.lesson
        lesson_progress = in_progress
    else:
        # Step 2: Find first lesson not started
        # Get all user's progress lesson IDs
        completed_or_started_lesson_ids = db.query(UserProgress.lesson_id).filter(
            UserProgress.user_id == current_user.id
        ).all()
        completed_ids = [lid[0] for lid in completed_or_started_lesson_ids]
        
        # Find first unstarted lesson (start with HSK 1)
        lesson = db.query(Lesson).filter(
            Lesson.is_published == True,
            ~Lesson.id.in_(completed_ids) if completed_ids else True
        ).order_by(Lesson.hsk_level, Lesson.order).first()
        
        if not lesson:
            # Step 3: All lessons completed, return the last accessed one
            last_progress = db.query(UserProgress).filter(
                UserProgress.user_id == current_user.id
            ).order_by(desc(UserProgress.last_accessed_at)).first()
            
            if last_progress and last_progress.lesson:
                lesson = last_progress.lesson
                lesson_progress = last_progress
            else:
                # Fallback: return first lesson of HSK 1
                lesson = db.query(Lesson).filter(
                    Lesson.hsk_level == 1,
                    Lesson.is_published == True
                ).order_by(Lesson.order).first()
                
                if not lesson:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="No lessons available"
                    )
                lesson_progress = None
        else:
            lesson_progress = None
    
    # Get lesson progress percent
    lesson_percent = lesson_progress.progress_percent if lesson_progress else 0.0
    
    # Step 4: Find first unfinished unit in the lesson
    # Get all units for this lesson
    units = db.query(Unit).filter(
        Unit.lesson_id == lesson.id
    ).order_by(Unit.order).all()
    
    if not units:
        # No units defined - create default vocabulary unit
        current_unit = None
        unit_id = f"unit_{lesson.id}_1"
        unit_type = "vocabulary"
        unit_order = 1
        unit_percent = 0.0
    else:
        # Get user's progress for these units
        unit_ids = [u.id for u in units]
        unit_progress_records = db.query(UnitProgress).filter(
            UnitProgress.user_id == current_user.id,
            UnitProgress.unit_id.in_(unit_ids)
        ).all()
        
        unit_progress_map = {up.unit_id: up for up in unit_progress_records}
        
        # Find first unfinished unit
        current_unit = None
        for u in units:
            up = unit_progress_map.get(u.id)
            if not up or not up.completed:
                current_unit = u
                unit_percent = up.progress_percent if up else 0.0
                break
        
        if not current_unit:
            # All units completed, return last unit
            current_unit = units[-1]
            up = unit_progress_map.get(current_unit.id)
            unit_percent = 100.0
        
        unit_id = f"unit_{lesson.id}_{current_unit.order}"
        unit_type = current_unit.type
        unit_order = current_unit.order
    
    # Build navigation info
    screen_name = UNIT_TYPE_SCREENS.get(unit_type, "LessonDetail")
    
    return LearningResumeResponse(
        course=CourseInfo(
            id=f"hsk{lesson.hsk_level}",
            level=get_hsk_level_name(lesson.hsk_level)
        ),
        lesson=LessonInfo(
            id=f"lesson_{lesson.id}",
            title=lesson.title,
            description=lesson.description
        ),
        unit=ResumeUnitInfo(
            id=unit_id,
            type=unit_type,
            order=unit_order
        ),
        progress=ResumeProgressInfo(
            lessonPercent=lesson_percent,
            unitPercent=unit_percent
        ),
        navigation=ResumeNavigationInfo(
            screen=screen_name,
            params={
                "lessonId": f"lesson_{lesson.id}",
                "unitId": unit_id
            }
        )
    )


@router.post("/track", status_code=status.HTTP_200_OK)
def track_item_progress(
    request: TrackItemRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Đánh dấu một mục nội dung (từ vựng, ví dụ ngữ pháp, v.v.) đã được người dùng học/truy cập.
    """
    # Tìm hoặc tạo bản ghi tiến độ cho item này
    item_progress = db.query(UserItemProgress).filter(
        UserItemProgress.user_id == current_user.id,
        UserItemProgress.item_type == request.item_type,
        UserItemProgress.item_id == request.item_id
    ).first()
    
    if not item_progress:
        item_progress = UserItemProgress(
            user_id=current_user.id,
            item_type=request.item_type,
            item_id=request.item_id,
            completed=request.completed
        )
        db.add(item_progress)
    else:
        item_progress.completed = request.completed
        # Cập nhật thời gian truy cập cuối (tự động qua onupdate)
    
    # Force flush to ensure the count query below includes this change
    db.flush()
    
    # -------------------------------------------------------------
    # PROGRESS CALCULATION LOGIC
    # -------------------------------------------------------------
    # Step 1: Find corresponding lesson IDs based on item tracked
    lesson_ids = []
    if request.item_type == "vocabulary":
        # Get all lessons that contain this vocabularyword through the association table
        lessons_with_vocab = db.query(lesson_vocabulary.c.lesson_id).filter(
            lesson_vocabulary.c.vocabulary_id == request.item_id
        ).all()
        lesson_ids = [l[0] for l in lessons_with_vocab]
    elif request.item_type == "grammar_example":
        from models.lesson import GrammarExample, GrammarPoint
        # GrammarExample -> GrammarPoint -> Lesson
        ge = db.query(GrammarExample).filter(GrammarExample.id == request.item_id).first()
        if ge:
            gp = db.query(GrammarPoint).filter(GrammarPoint.id == ge.grammar_point_id).first()
            if gp:
                lesson_ids = [gp.lesson_id]
    elif request.item_type == "listening" or request.item_type == "speaking":
        from models.unit import Unit
        u = db.query(Unit).filter(Unit.id == request.item_id).first()
        if u:
            lesson_ids = [u.lesson_id]
    elif request.item_type == "lesson":
        lesson_ids = [request.item_id]
            
    # Step 2: Recalculate if lessons found
    for lesson_id in lesson_ids:
        if request.item_type == "lesson":
            # Explicitly marking a lesson as completed
            new_progress = 100 if request.completed else 0
        else:
            # Aggregate progress across all item types in this lesson
            # 1. Vocab
            all_vocab = db.query(lesson_vocabulary.c.vocabulary_id).filter(
                lesson_vocabulary.c.lesson_id == lesson_id
            ).all()
            vocab_ids = list(set([v[0] for v in all_vocab]))
            
            # 2. Grammar Examples
            from models.lesson import GrammarPoint, GrammarExample
            all_ge = db.query(GrammarExample.id).join(GrammarPoint).filter(
                GrammarPoint.lesson_id == lesson_id
            ).all()
            ge_ids = [g[0] for g in all_ge]
            
            # 3. Units (Listening/Speaking)
            from models.unit import Unit
            all_u = db.query(Unit.id).filter(Unit.lesson_id == lesson_id).all()
            unit_ids = [u[0] for u in all_u]
            
            total_items = len(vocab_ids) + len(ge_ids) + len(unit_ids)
            
            if total_items > 0:
                # Count completed items
                c_vocab = db.query(UserItemProgress).filter(
                    UserItemProgress.user_id == current_user.id,
                    UserItemProgress.item_type == "vocabulary",
                    UserItemProgress.item_id.in_(vocab_ids),
                    UserItemProgress.completed == True
                ).count() if vocab_ids else 0
                
                c_ge = db.query(UserItemProgress).filter(
                    UserItemProgress.user_id == current_user.id,
                    UserItemProgress.item_type == "grammar_example",
                    UserItemProgress.item_id.in_(ge_ids),
                    UserItemProgress.completed == True
                ).count() if ge_ids else 0
                
                c_u = db.query(UserItemProgress).filter(
                    UserItemProgress.user_id == current_user.id,
                    UserItemProgress.item_type.in_(["listening", "speaking"]),
                    UserItemProgress.item_id.in_(unit_ids),
                    UserItemProgress.completed == True
                ).count() if unit_ids else 0
                
                completed_count = c_vocab + c_ge + c_u
                new_progress = round((completed_count / total_items) * 100)
                new_progress = min(100, new_progress)
            else:
                new_progress = 100 if request.completed else 0
            
            # Update UserProgress table
            user_progress = db.query(UserProgress).filter(
                UserProgress.user_id == current_user.id,
                UserProgress.lesson_id == lesson_id
            ).first()
            
            if not user_progress:
                user_progress = UserProgress(
                    user_id=current_user.id,
                    lesson_id=lesson_id,
                    progress_percent=new_progress,
                    completed=(new_progress >= 100.0)
                )
                db.add(user_progress)
            else:
                user_progress.progress_percent = new_progress
                user_progress.completed = (new_progress >= 100.0)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error tracking item progress: {str(e)}"
        )
    
    return {"status": "success", "message": f"Tracked {request.item_type} {request.item_id}"}


