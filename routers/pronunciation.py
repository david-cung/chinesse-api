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

from database.database import get_db
from models.user import User
from utils.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/pronunciation", tags=["pronunciation"])

# Configure Gemini API
API_KEY = os.getenv("API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)


class PronunciationScoreResponse(BaseModel):
    """Response trả về điểm phát âm"""
    score: float  # Điểm từ 0-100
    feedback: str  # Nhận xét chi tiết
    detected_text: Optional[str] = None  # Văn bản nhận diện được
    pronunciation_issues: list[str] = []  # Các vấn đề về phát âm


@router.post("/score", response_model=PronunciationScoreResponse)
async def score_pronunciation(
    expected_text: str = Form(..., description="Văn bản tiếng Trung cần đọc"),
    expected_pinyin: Optional[str] = Form(None, description="Pinyin tham khảo"),
    audio: Optional[UploadFile] = File(None, description="File âm thanh (mp3, wav, webm, m4a)"),
    audio_base64: Optional[str] = Form(None, description="Audio dạng base64 (thay thế cho file)"),
    mime_type: str = Form("audio/webm", description="MIME type của audio (dùng khi gửi base64)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chấm điểm phát âm tiếng Trung của người dùng.
    
    Gửi audio bằng một trong hai cách:
    - Upload file: Sử dụng parameter `audio`
    - Base64 string: Sử dụng parameter `audio_base64` + `mime_type`
    
    Response trả về điểm số (0-100%) và nhận xét chi tiết.
    """
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="API_KEY chưa được cấu hình. Vui lòng kiểm tra file .env"
        )
    
    # Validate: phải có ít nhất 1 trong 2 loại input
    if not audio and not audio_base64:
        raise HTTPException(
            status_code=400,
            detail="Vui lòng gửi audio (file upload hoặc base64)"
        )
    
    try:
        # Xử lý audio data
        if audio:
            # File upload
            audio_bytes = await audio.read()
            audio_mime = audio.content_type or "audio/webm"
            audio_data = base64.b64encode(audio_bytes).decode("utf-8")
        else:
            # Base64 input
            audio_data = audio_base64
            audio_mime = mime_type
            # Clean base64 string (remove data URL prefix if present)
            if "," in audio_data:
                audio_data = audio_data.split(",")[1]
        
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

        # Create audio part
        audio_part = {
            "inline_data": {
                "mime_type": audio_mime,
                "data": audio_data
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
