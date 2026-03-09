from pydantic import Field
from sqlalchemy.sql.annotation import Annotated

from src.domain.constants import card_constants as card

def get_masked_card_number(card_number: str) -> str:
    if len(card_number) != card.CARD_VISIBLE_DIGITS:
        return card_number

    visible_part = card_number[-card.CARD_MASK_VISIBLE_END:] # last 4 numbers
    mask_length = card.CARD_NUMBER_LENGTH - card.CARD_MASK_VISIBLE_END # first 12 masked digits
    masked_card_number = card.CARD_MASK_CHAR * mask_length

    return f"{masked_card_number}{visible_part}"

CardNumberLength = Annotated[
    str,
    Field(
        min_length=card.CARD_NUMBER_LENGTH,
        max_length=card.CARD_NUMBER_LENGTH,
        pattern=r"^\d+$"
    )
]