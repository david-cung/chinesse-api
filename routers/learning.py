from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional
from database.database import get_db
from models.user import User
from models.lesson import Lesson
from models.progress import UserProgress
from schemas.schemas import (
    LearningContinueResponse, 
    CourseInfo, 
    LessonInfo, 
    ProgressInfo
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
