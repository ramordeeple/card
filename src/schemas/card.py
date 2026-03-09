import uuid
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from src.db.models import card

CardNumberLength = Annotated[
    str,
    Field(
        min_length=card.CARD_NUMBER_LENGTH,
        max_length=card.CARD_NUMBER_LENGTH,
        pattern=r"^\d+$"
    )
]

class CardRead(BaseModel):
    id: uuid.UUID
    balance: Decimal
    number_masked: str

    model_config = ConfigDict(from_attributes=True)

class CardCreate(BaseModel):
    owner_id: uuid.UUID
    number: CardNumberLength