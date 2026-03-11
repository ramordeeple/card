import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, String, DateTime, Enum as sqlalchemy_enum
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.db.session import Base
from src.domain.constants.card_constants import CARD_ENCRYPTED_MAX_LENGTH
from src.domain.enums.card_status import CardStatus

if TYPE_CHECKING:
    from src.db.models.user import User

class Card(Base):
    __tablename__ = 'cards'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    number_encrypted: Mapped[str] = mapped_column(String(CARD_ENCRYPTED_MAX_LENGTH), unique=True, nullable=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id', ondelete='RESTRICT'), nullable=False)
    expiration_date: Mapped[date] = mapped_column(DateTime, nullable=False)
    status: Mapped[int] = mapped_column(
        sqlalchemy_enum(CardStatus),
        default=CardStatus.ACTIVE,
        nullable=False
    )

    owner: Mapped['User'] = relationship('User', back_populates='cards')
