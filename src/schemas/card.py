import uuid
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, computed_field

from src.domain.constants import card_constants
from src.domain.constants.card_constants import (
    CARD_MASK_TEMPLATE,
)
from src.domain.enums.card_status import CardStatus

CardNumberLength = Annotated[
    str,
    Field(
        min_length=card_constants.CARD_NUMBER_LENGTH,
        max_length=card_constants.CARD_NUMBER_LENGTH,
        pattern=r"^\d+$",
    ),
]


class CardRead(BaseModel):
    id: uuid.UUID
    balance: Decimal
    status: CardStatus

    number_last4: str = Field(exclude=True)

    @computed_field
    def number_masked(self) -> str:
        return f"{CARD_MASK_TEMPLATE}{self.number_last4}"

    model_config = ConfigDict(from_attributes=True)

class TransferRequest(BaseModel):
    from_id: uuid.UUID
    to_id: uuid.UUID
    amount: Decimal

class CardDeposit(BaseModel):
    amount: Decimal = Field(gt=0, decimal_places=2, description='Amount to deposit')

class CardlistResponse(BaseModel):
    items: list[CardRead]
    total: int
    limit: int
    offset: int
