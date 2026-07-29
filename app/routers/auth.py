from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models
from app.auth import create_access_token, hash_password, verify_password
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

class UserCreate(BaseModel):
    email: str
    password: str

@router.post("/register", status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(models.User).filter(
        models.User.email == payload.email
    ).first()
    if exists:
        raise HTTPException(409, "Email already registered")
    user = models.User(
        email = payload.email,
        hashed_password=hash_password(payload.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "email": user.email}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == form.username
    ).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Incorrect email or password")
    return {"access_token": create_access_token(user.id), "token_type": "bearer"}