
from dotenv import load_dotenv
load_dotenv()  

from fastapi import FastAPI
from routers import auth, predict, news
from database import Base, engine
from models import user, predictor
from fastapi.middleware.cors import CORSMiddleware
from routers.chatbot import router as chatbot_router
from fastapi.staticfiles import StaticFiles
from models.user import User
from pathlib import Path



app = FastAPI(title="Healthify API")

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(news.router)
app.include_router(chatbot_router)

# 1) Bu dosyanın (main.py) bulunduğu klasör
HERE = Path(__file__).resolve().parent

# 2) Projenin kök klasörü (örneğin main.py 'backend' içinde ise bir üst klasöre çık)
PROJECT_ROOT = HERE.parent

# 3) frontend dizini
FRONTEND_DIR = PROJECT_ROOT / "frontend"

# Statik frontend dosyalarını serve et
app.mount(
    "/",
    StaticFiles(directory=str(FRONTEND_DIR), html=True),
    name="frontend"
)

Base.metadata.create_all(bind=engine)
