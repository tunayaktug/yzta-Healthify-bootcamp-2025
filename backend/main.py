from fastapi import FastAPI
from backend.routers import auth, predict
from backend.database import Base, engine

app = FastAPI()
app.include_router(auth.router)
app.include_router(predict.router)

Base.metadata.create_all(bind=engine)  # db yoksa dbyi oluşturuyoruz



