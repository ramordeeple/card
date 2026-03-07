from datetime import timezone, datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from src.core.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject: str, expires_delta: datetime.timedelta = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)

    to_encode = {'exp': expire, 'sub': str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        settings.JWT_ALGORITHM
    )

    return encoded_jwt