import uuid
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, String, DateTime, Enum as sqlalchemy_enum, Numeric, LargeBinary
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.db.session import Base
from src.domain.constants.card_constants import CARD_ENCRYPTED_MAX_LENGTH, CARD_MASK_VISIBLE_END
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
    number_encrypted: Mapped[bytes] = mapped_column(LargeBinary, unique=True, nullable=False)
    number_last4: Mapped[str] = mapped_column(String(CARD_MASK_VISIBLE_END), nullable=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(precision=15, scale=2), default=Decimal('0.00'))
    expiration_date: Mapped[date] = mapped_column(DateTime, nullable=False)
    status: Mapped[int] = mapped_column(
        sqlalchemy_enum(CardStatus),
        default=CardStatus.ACTIVE,
        nullable=False
    )

    owner: Mapped['User'] = relationship('User', back_populates='cards')
