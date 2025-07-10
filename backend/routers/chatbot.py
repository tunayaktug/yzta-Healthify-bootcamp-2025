# routers/chatbot.py

import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Google Generative AI import
import google.generativeai as genai
# ENV’den API anahtarınızı çekin
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY bulunamadı!")

# Yeni SDK ile yapılandırma
import google.generativeai as genai
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

class ChatRequest(BaseModel):
    message: str
    ilaclar: str = ""
    ameliyatlar: str = ""

class ChatResponse(BaseModel):
    reply: str

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Tek‐sıralı bir prompt ile Gemini 2.5‐Flash modelinden
    Türkçe “doktor” cevabı alır.
    """
    try:
        # Sistem + kullanıcı satırı
        prompt = (
            "Sen bir doktor gibi konuşan yapay zekasın. Adın Dr. Bilge. "
            "Hastaların sorularını Türkçe, nazik ve bilgilendirici şekilde yanıtla. "
            "Tıbbi tavsiyelerini güvenilir kaynaklara dayandır ve önleyici sağlık önerileri sun.\n\n"
            f"Kullanıcının geçmiş sağlık bilgileri:\n"
            f"- Kullandığı ilaçlar: {request.ilaclar or 'bilgi verilmedi'}\n"
            f"- Geçirdiği ameliyatlar: {request.ameliyatlar or 'bilgi verilmedi'}\n\n"
            f"Soru: {request.message}"
        )

        # Doğru SDK ile içerik üretimi
        response = model.generate_content(prompt)
        return ChatResponse(reply=response.text.strip())

    except Exception as e:
        import traceback; print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"API hatası: {e}")
