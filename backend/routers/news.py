import os
import json
import time
import requests
from fastapi import APIRouter

router = APIRouter(
    prefix="/news",
    tags=["News"]
)

# Cache dosyasının yolunu proje köküne ayarla
CACHE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'news_cache.json'))
print("Cache dosyası yolu:", CACHE_FILE)
CACHE_DURATION = 60 * 60  # 1 saat (saniye cinsinden)

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return None, 0
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("news"), data.get("timestamp", 0)
    except Exception:
        return None, 0

def save_cache(news, timestamp):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({"news": news, "timestamp": timestamp}, f)

@router.get("")
def get_health_news():
    # 1. Dosyadan cache oku
    news_cache, cache_timestamp = load_cache()
    now = time.time()
    # 2. Cache güncelse, onu döndür
    if news_cache is not None and (now - cache_timestamp) < CACHE_DURATION:
        return news_cache
    # 3. Değilse API'den çek, cache'i güncelle ve dosyaya yaz
    url = "https://newsdata.io/api/1/news?apikey=pub_d97d98cf92414c0b9d55a9aafc08e11b&country=tr&language=tr&category=health"
    response = requests.get(url)
    news_cache = response.json()
    save_cache(news_cache, now)
    return news_cache
