from typing import TYPE_CHECKING
from datetime import datetime
import uuid

import sqlalchemy
from sqlalchemy import String, UUID, Enum as sqlalchemy_enum, DateTime
from sqlalchemy.orm import Mapped, relationship, mapped_column

if TYPE_CHECKING:
    from src.db.models.card import Card

from src.db.session import Base
from src.domain.constants.user_constants import USERNAME_MAX_LENGTH, PASSWORD_HASH_MAX_LENGTH
from src.domain.enums.user_role import UserRole

class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(USERNAME_MAX_LENGTH), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(PASSWORD_HASH_MAX_LENGTH), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        sqlalchemy_enum(UserRole),
        default=UserRole.USER,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=sqlalchemy.func.now()
    )

    cards: Mapped[list['Card']] = relationship('Card', back_populates='owner')



