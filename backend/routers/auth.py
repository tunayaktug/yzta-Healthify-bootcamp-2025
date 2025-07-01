from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import user as models
from database import get_db
from utils.hash_handler import hash_password
from pydantic import BaseModel, EmailStr
from utils.jwt_handler import create_access_token, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name : str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(models.User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(request.password)

    new_user = models.User(email=request.email, password=hashed_pw, name=request.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user.email})
    return {
    "access_token": access_token,
    "token_type": "bearer",
    "name": user.name  # <-- Kullanıcının adı ekleniyor
}
