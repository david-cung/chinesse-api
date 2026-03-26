from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
import google.generativeai as genai
import os
import base64

from database.database import get_db
from models.user import User
from utils.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/ai", tags=["ai"])

# Configure Gemini API
API_KEY = os.getenv("API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)


class Message(BaseModel):
    role: str # "user" or "model" (or "assistant")
    content: str


class ChatRequest(BaseModel):
    message: str
    history: List[Message] = []


class ChatResponse(BaseModel):
    response: str
    pinyin: str
    translation: str


@router.post("/chat", response_model=ChatResponse)
async def ai_chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat với AI (vai giáo viên tiếng Trung).
    """
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="API_KEY chưa được cấu hình. Vui lòng kiểm tra file .env"
        )
    
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        system_instruction = """Bạn là một người bản xứ tiếng Trung thân thiện đang trò chuyện với một người học tiếng Trung ở trình độ HSK 1-2.
Luôn thực hiện theo các nguyên tắc sau:
1. Phát ngôn của bạn phải RẤT NGẮN GỌN (1-2 câu đơn giản), dùng từ vựng HSK 1-2 cơ bản.
2. Bạn phải trả lời bằng định dạng JSON độc nhất theo cấu trúc sau (không có bất cứ text nào khác ở ngoài JSON):
{
  "response": "<câu trả lời bằng tiếng Trung giản thể>",
  "pinyin": "<pinyin của câu trả lời, có thanh điệu số hoặc ký hiệu thanh điệu>",
  "translation": "<bản dịch tiếng Việt tự nhiên của câu trả lời>"
}
3. Cư xử tự nhiên như một đối tác hội thoại. Bắt đầu câu chuyện hoặc tiếp tục theo luồng hội thoại của người dùng."""

        # Chuyển đổi lịch sử chat sang định dạng của Gemini
        gemini_history = []
        for msg in request.history:
            role = "user" if msg.role == "user" else "model"
            gemini_history.append({"role": role, "parts": [msg.content]})
            
        chat = model.start_chat(history=gemini_history)
        
        # Combine system instruction with the prompt on the first turn or implicitly by instructing in the prompt
        full_prompt = f"{system_instruction}\n\nNgười dùng nói: {request.message}\nPhản hồi JSON:"
        
        response = chat.send_message(full_prompt)
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
            return ChatResponse(
                response="对不起，我没听懂。(Xin lỗi, tôi không hiểu rõ.)",
                pinyin="Duìbuqǐ, wǒ méi tīng dǒng.",
                translation="Xin lỗi, tôi không hiểu rõ."
            )
            
        return ChatResponse(
            response=result.get("response", ""),
            pinyin=result.get("pinyin", ""),
            translation=result.get("translation", "")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi chat với AI: {str(e)}"
        )
