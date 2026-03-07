from http.client import HTTPException

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.security import hash_password
from src.db.models.user import User
from src.db.session import SessionLocal
from src.schemas.user import UserCreate, UserRead

router = APIRouter(prefix='/auth', tags=['Auth'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/register', response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    result = db.execute(select(User).where(User.username == user_in.username))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Such user already exists'
        )

    new_user = User(
        username=user_in.username,
        hashed_password=hash_password(user_in.password),
        role=user_in.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


