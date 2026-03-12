from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import random

from database.database import get_db
from models.lesson import Lesson, Vocabulary, Exercise
from models.quiz import QuizAttempt, WordStats
from models.sentence import Sentence
from schemas import schemas
from utils.dependencies import get_current_user
from models.user import User

router = APIRouter(
    prefix="/api/v1/quiz",
    tags=["quiz"]
)

@router.get("/multiple-choice/{lesson_id}", response_model=List[schemas.MultipleChoiceQuestion])
def get_multiple_choice_quiz(
    lesson_id: int,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate multiple choice questions for a lesson (Chinese <-> English)"""
    vocab_list = db.query(Vocabulary).join(Vocabulary.lessons).filter(Lesson.id == lesson_id).all()
    
    if not vocab_list:
        raise HTTPException(status_code=404, detail="No vocabulary found for this lesson")
    
    questions = []
    sample_size = min(len(vocab_list), limit)
    selected_vocab = random.sample(vocab_list, sample_size)
    
    # All meanings for distractors
    all_meanings = [v.meaning for v in vocab_list]
    all_words = [v.word for v in vocab_list]
    
    for vocab in selected_vocab:
        is_zh_to_en = random.choice([True, False])
        
        if is_zh_to_en:
            correct_answer = vocab.meaning
            distractors = [m for m in all_meanings if m != correct_answer]
            type_str = "zh_to_en"
            question_text = vocab.word
        else:
            correct_answer = vocab.word
            distractors = [w for w in all_words if w != correct_answer]
            type_str = "en_to_zh"
            question_text = vocab.meaning
            
        # Select 3 unique distractors
        if len(distractors) >= 3:
            distractors = random.sample(distractors, 3)
        
        options = distractors + [correct_answer]
        random.shuffle(options)
        
        questions.append({
            "id": f"mcq_{vocab.id}_{type_str}",
            "vocabulary_id": vocab.id,
            "question": question_text,
            "correct_answer": correct_answer,
            "options": options,
            "type": type_str
        })
        
    return questions

@router.get("/matching/{lesson_id}", response_model=schemas.MatchingGameResponse)
def get_matching_game(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate matching pairs for a lesson"""
    vocab_list = db.query(Vocabulary).join(Vocabulary.lessons).filter(Lesson.id == lesson_id).all()
    
    if len(vocab_list) < 4:
        # If too few words in lesson, get more from same HSK level
        lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        vocab_list = db.query(Vocabulary).filter(Vocabulary.hsk_level == lesson.hsk_level).limit(8).all()

    sample_size = min(len(vocab_list), 6)
    selected = random.sample(vocab_list, sample_size)
    
    pairs = []
    for v in selected:
        pairs.append({
            "zh": v.word,
            "en": v.meaning,
            "vocabulary_id": v.id
        })
        
    return {"pairs": pairs}

@router.get("/sentence/{lesson_id}", response_model=List[schemas.SentenceGameQuestion])
def get_sentence_quiz(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate sentence building questions for a lesson"""
    sentences = db.query(Sentence).filter(Sentence.lesson_id == lesson_id).all()
    
    if not sentences:
        # Fallback to vocabulary examples if no specific sentences
        vocab_list = db.query(Vocabulary).join(Vocabulary.lessons).filter(Lesson.id == lesson_id).all()
        # This part would be more complex, but for now return empty or mock
        return []
    
    questions = []
    for s in sentences:
        # Simple word splitting for Chinese (needs better segmenter in production)
        # For now, treat each character as a tile or use a simple split
        words = list(s.characters) # Each character is a tile
        random.shuffle(words)
        
        questions.append({
            "sentence_id": s.id,
            "characters": s.characters,
            "pinyin": s.pinyin,
            "meaning": s.meaning,
            "words": words
        })
        
    return questions

@router.post("/submit", response_model=schemas.QuizAttemptResponse)
def submit_quiz_result(
    result: schemas.QuizAttemptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit quiz result and update word stats"""
    attempt = QuizAttempt(
        user_id=current_user.id,
        **result.dict()
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    
    return attempt
