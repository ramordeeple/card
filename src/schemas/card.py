import uuid
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from src.domain.rules.card_rules import CardNumberLength


class CardRead(BaseModel):
    id: uuid.UUID
    balance: Decimal
    number_masked: str

    model_config = ConfigDict(from_attributes=True)

class CardCreate(BaseModel):
    owner_id: uuid.UUID
    number: CardNumberLength