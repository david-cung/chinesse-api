# routers/pronunciation.py
"""
API chấm điểm phát âm tiếng Trung sử dụng Google Gemini Flash API
"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai
import os
import base64
import tempfile

from database.database import get_db
from models.user import User
from utils.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/pronunciation", tags=["pronunciation"])

# Configure Gemini API
API_KEY = os.getenv("API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)


class PronunciationScoreRequest(BaseModel):
    """Request body for text-based pronunciation check"""
    expected_text: str  # Văn bản tiếng Trung cần đọc
    expected_pinyin: Optional[str] = None  # Pinyin tham khảo


class PronunciationScoreResponse(BaseModel):
    """Response trả về điểm phát âm"""
    score: float  # Điểm từ 0-100
    feedback: str  # Nhận xét chi tiết
    detected_text: Optional[str] = None  # Văn bản nhận diện được
    pronunciation_issues: list[str] = []  # Các vấn đề về phát âm


@router.post("/score", response_model=PronunciationScoreResponse)
async def score_pronunciation(
    audio: UploadFile = File(..., description="File âm thanh (mp3, wav, webm, m4a)"),
    expected_text: str = Form(..., description="Văn bản tiếng Trung cần đọc"),
    expected_pinyin: Optional[str] = Form(None, description="Pinyin tham khảo"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chấm điểm phát âm tiếng Trung của người dùng.
    
    - Upload file âm thanh ghi âm của người dùng
    - Gửi lên Google Gemini Flash API để phân tích
    - Trả về điểm số (0-100%) và nhận xét chi tiết
    """
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="API_KEY chưa được cấu hình. Vui lòng kiểm tra file .env"
        )
    
    # Validate file type
    allowed_types = ["audio/mpeg", "audio/wav", "audio/webm", "audio/x-m4a", "audio/mp4", "audio/ogg"]
    if audio.content_type and audio.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Định dạng file không hỗ trợ. Chấp nhận: mp3, wav, webm, m4a. Nhận được: {audio.content_type}"
        )
    
    try:
        # Read audio file
        audio_bytes = await audio.read()
        
        # Determine mime type
        mime_type = audio.content_type or "audio/webm"
        
        # Create Gemini model
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        # Create the prompt for pronunciation scoring
        prompt = f"""Bạn là một giáo viên tiếng Trung chuyên nghiệp. Hãy nghe đoạn ghi âm và chấm điểm phát âm.

Văn bản cần đọc: {expected_text}
{f"Pinyin tham khảo: {expected_pinyin}" if expected_pinyin else ""}

Yêu cầu:
1. Nhận diện văn bản người dùng đã đọc
2. So sánh với văn bản cần đọc
3. Đánh giá các yếu tố:
   - Độ chính xác của thanh điệu (rất quan trọng trong tiếng Trung)
   - Độ rõ ràng của phụ âm và nguyên âm
   - Nhịp điệu và tốc độ nói
   - Độ tự nhiên của giọng nói

Trả lời theo định dạng JSON sau (CHỈ trả về JSON, không có text khác):
{{
  "score": <điểm từ 0 đến 100>,
  "detected_text": "<văn bản nhận diện được từ audio>",
  "feedback": "<nhận xét tổng quan bằng tiếng Việt, 1-2 câu>",
  "pronunciation_issues": ["<vấn đề 1>", "<vấn đề 2>"]
}}

Lưu ý:
- Nếu không nghe được gì hoặc audio trống, cho điểm 0
- Nếu đọc gần đúng nhưng sai thanh điệu, trừ 10-30 điểm
- Nếu đọc sai từ, trừ nhiều điểm hơn
- Phản hồi bằng tiếng Việt để người dùng dễ hiểu"""

        # Upload audio as inline data
        audio_part = {
            "inline_data": {
                "mime_type": mime_type,
                "data": base64.b64encode(audio_bytes).decode("utf-8")
            }
        }
        
        # Call Gemini API
        response = model.generate_content([prompt, audio_part])
        
        # Parse response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        import json
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            # If JSON parsing fails, return a default response
            return PronunciationScoreResponse(
                score=0,
                feedback="Không thể phân tích phản hồi từ AI. Vui lòng thử lại.",
                detected_text=None,
                pronunciation_issues=["Lỗi xử lý phản hồi"]
            )
        
        return PronunciationScoreResponse(
            score=min(100, max(0, float(result.get("score", 0)))),
            feedback=result.get("feedback", "Không có nhận xét"),
            detected_text=result.get("detected_text"),
            pronunciation_issues=result.get("pronunciation_issues", [])
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi xử lý âm thanh: {str(e)}"
        )


@router.post("/score-base64", response_model=PronunciationScoreResponse)
async def score_pronunciation_base64(
    audio_base64: str = Form(..., description="Audio data dạng base64"),
    mime_type: str = Form("audio/webm", description="MIME type của audio"),
    expected_text: str = Form(..., description="Văn bản tiếng Trung cần đọc"),
    expected_pinyin: Optional[str] = Form(None, description="Pinyin tham khảo"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chấm điểm phát âm tiếng Trung với audio dạng base64.
    
    Dùng cho trường hợp frontend gửi audio đã encode base64.
    """
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="API_KEY chưa được cấu hình. Vui lòng kiểm tra file .env"
        )
    
    try:
        # Create Gemini model
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        # Create the prompt
        prompt = f"""Bạn là một giáo viên tiếng Trung chuyên nghiệp. Hãy nghe đoạn ghi âm và chấm điểm phát âm.

Văn bản cần đọc: {expected_text}
{f"Pinyin tham khảo: {expected_pinyin}" if expected_pinyin else ""}

Yêu cầu:
1. Nhận diện văn bản người dùng đã đọc
2. So sánh với văn bản cần đọc
3. Đánh giá các yếu tố:
   - Độ chính xác của thanh điệu (rất quan trọng trong tiếng Trung)
   - Độ rõ ràng của phụ âm và nguyên âm
   - Nhịp điệu và tốc độ nói
   - Độ tự nhiên của giọng nói

Trả lời theo định dạng JSON sau (CHỈ trả về JSON, không có text khác):
{{
  "score": <điểm từ 0 đến 100>,
  "detected_text": "<văn bản nhận diện được từ audio>",
  "feedback": "<nhận xét tổng quan bằng tiếng Việt, 1-2 câu>",
  "pronunciation_issues": ["<vấn đề 1>", "<vấn đề 2>"]
}}

Lưu ý:
- Nếu không nghe được gì hoặc audio trống, cho điểm 0
- Nếu đọc gần đúng nhưng sai thanh điệu, trừ 10-30 điểm
- Nếu đọc sai từ, trừ nhiều điểm hơn
- Phản hồi bằng tiếng Việt để người dùng dễ hiểu"""

        # Clean base64 string (remove data URL prefix if present)
        if "," in audio_base64:
            audio_base64 = audio_base64.split(",")[1]
        
        # Create audio part
        audio_part = {
            "inline_data": {
                "mime_type": mime_type,
                "data": audio_base64
            }
        }
        
        # Call Gemini API
        response = model.generate_content([prompt, audio_part])
        
        # Parse response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        import json
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            return PronunciationScoreResponse(
                score=0,
                feedback="Không thể phân tích phản hồi từ AI. Vui lòng thử lại.",
                detected_text=None,
                pronunciation_issues=["Lỗi xử lý phản hồi"]
            )
        
        return PronunciationScoreResponse(
            score=min(100, max(0, float(result.get("score", 0)))),
            feedback=result.get("feedback", "Không có nhận xét"),
            detected_text=result.get("detected_text"),
            pronunciation_issues=result.get("pronunciation_issues", [])
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi xử lý âm thanh: {str(e)}"
        )
