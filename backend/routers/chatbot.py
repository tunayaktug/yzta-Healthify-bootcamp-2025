# routers/chatbot.py

import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Yeni SDK’dan import
from google import genai
from google.genai import types

# ENV’den API anahtarınızı çekin
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY bulunamadı!")

# Client’ı örnekleyin (SDK, env’den okuduğu için parametre de atlamazsınız)
client = genai.Client(api_key=API_KEY)

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


        # Tek satırlık içerik üretimi
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        # Yanıtı dön
        return ChatResponse(reply=response.text.strip())

    except Exception as e:
        # Hata detayını debug için konsola basabilirsiniz:
        # import traceback; print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"API hatası: {e}")
