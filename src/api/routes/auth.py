from http.client import HTTPException

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.security.hashing import hash_password, verify_password
from src.core.security.jwt import create_access_token
from src.db.models.user import User
from src.db.session import SessionLocal
from src.domain.enums.user_role import UserRole
from src.schemas.user import UserCreate, UserRead, Token

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
        role=UserRole.USER,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post('/login', response_model=Token)
def login(user_in: UserCreate, db: Session = Depends(get_db)):
    result = db.execute(select(User).where(User.username == user_in.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    access_token = create_access_token(subject=user.id)

    return {'access_token': access_token, 'token_type': 'bearer'}
