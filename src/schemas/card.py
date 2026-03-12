import uuid
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, computed_field

from src.domain.constants import card_constants
from src.domain.constants.card_constants import CARD_MASK_VISIBLE_END, CARD_MASK_TEMPLATE
from src.domain.enums.card_status import CardStatus

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
    status: CardStatus

    @computed_field
    def number_masked(self) -> str:
        last_four = str(self.balance)[-CARD_MASK_VISIBLE_END:]

        return f"{CARD_MASK_TEMPLATE}{last_four}"

    model_config = ConfigDict(from_attributes=True)

class CardCreate(BaseModel):
    owner_id: uuid.UUID
    number: CardNumberLength