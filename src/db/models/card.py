from datetime import date

from sqlalchemy import ForeignKey, String, DateTime, Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from src.db.session import Base
from src.domain.enums.card_status import CardStatus


class Card(Base):
    __tablename__ = 'card'

    id: Mapped[int] = mapped_column(primary_key=True)
    number_encrypted: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    expiration_date: Mapped[date] = mapped_column(DateTime, nullable=False)
    status: Mapped[int] = mapped_column(
        Enum(CardStatus),
        default=CardStatus.ACTIVE,
        nullable=False
    )

