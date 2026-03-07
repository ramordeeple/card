import uuid
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CardRead(BaseModel):
    id: uuid.UUID
    balance: Decimal
    number_masked: str

    model_config = ConfigDict(from_attributes=True)
