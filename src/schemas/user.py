import uuid

from pydantic import BaseModel, Field, ConfigDict

from src.domain.constants.user_constants import USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH, PASSWORD_MIN_LENGTH
from src.domain.enums.user_role import UserRole


class UserBase(BaseModel):
    username: str = Field(..., min_length=USERNAME_MIN_LENGTH, max_length=USERNAME_MAX_LENGTH)
    role: UserRole = UserRole.USER

class UserCreate(UserBase):
    password: str = Field(..., min_length=PASSWORD_MIN_LENGTH)

class UserRead(UserBase):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_toke: str
    token_type: str = 'bearer'
