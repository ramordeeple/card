from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException, status

from src.db.models.card import Card
from src.domain.enums.card_status import CardStatus


def validate_transaction_amount(amount: Decimal) -> None:
    if amount <= Decimal('0.00'):
        raise ValueError('Amount must be positive')

def check_card_existence(card: Card | None):
    if card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Card not found'
        )

def check_card_is_active(card: Card, card_name: str = 'Card'):
    if card.status != CardStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'{card_name} is not active'
        )

def check_card_is_blocked(card: Card):
    if card.status == CardStatus.BLOCKED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Card is already blocked'
        )

def check_card_access(card: Card | None, user_id: UUID):
    if not card or card.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Card not found'
        )