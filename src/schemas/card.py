import uuid
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from src.domain.constants import card_constants

CardNumberLength = Annotated[
    str,
    Field(
        min_length=card_constants.CARD_NUMBER_LENGTH,
        max_length=card_constants.CARD_NUMBER_LENGTH,
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