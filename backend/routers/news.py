# backend/routers/news.py
import requests
from fastapi import APIRouter
import time

router = APIRouter(
    prefix="/news",
    tags=["News"]
)

# Cache için değişkenler
news_cache = None
cache_timestamp = 0
CACHE_DURATION = 60 * 60  # 1 saat (saniye cinsinden)

@router.get("")
def get_health_news():
    global news_cache, cache_timestamp
    now = time.time()
    # Eğer cache güncelse, cache'i döndür
    if news_cache is not None and (now - cache_timestamp) < CACHE_DURATION:
        return news_cache
    # Değilse API'den çek ve cache'i güncelle
    url = "https://newsdata.io/api/1/news?apikey=pub_d97d98cf92414c0b9d55a9aafc08e11b&country=tr&language=tr&category=health"
    response = requests.get(url)
    news_cache = response.json()
    cache_timestamp = now
    return news_cache
