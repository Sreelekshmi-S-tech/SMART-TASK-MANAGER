from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

from auth import hash_password, verify_password, create_access_token

router = APIRouter()


# =========================
# REGISTER USER (FIXED)
# =========================
@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # check if username already exists
    existing_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # check if email already exists (extra safety)
    existing_email = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    hashed_pw = hash_password(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }
    }


# =========================
# LOGIN USER (JWT)
# =========================
@router.post("/login")
def login(user: dict, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(
        models.User.email == user["email"]
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )

    if not verify_password(user["password"], db_user.password):
        raise HTTPException(
            status_code=400,
            detail="Wrong password"
        )

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =========================
# TEST ROUTE
# =========================
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return {
        "message": "Users router working",
        "users": users
    }