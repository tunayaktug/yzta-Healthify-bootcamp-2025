from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.models import user as models
from backend.database import get_db
from backend.utils.hash_handler import hash_password
from pydantic import BaseModel, EmailStr


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str



@router.post("/register")
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(models.User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(request.password)

    new_user = models.User(email=request.email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}
