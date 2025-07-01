from fastapi import FastAPI
from routers import auth, predict
from database import Base, engine
from models import user, predictor
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()  

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

Base.metadata.create_all(bind=engine)

