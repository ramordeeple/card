import uuid

from pydantic import BaseModel, Field, ConfigDict

from src.domain.enums.user_role import UserRole


class UserBase(BaseModel):
    username: str = Field(..., min_length=4, max_length=50)
    role: UserRole = UserRole.USER

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserRead(UserBase):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_toke: str
    token_type: str = 'bearer'
