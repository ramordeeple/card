from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException, status

from src.db.models.card import Card

def check_both_cards_found(cards: list[Card]):
    if len(cards) < 2:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='One or both cards not found'
        )

def check_sufficient_funds(balance: Decimal, amount: Decimal):
    if balance < amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='Insufficient funds'
        )

def check_not_same_card(from_id: str, to_id: str):
    if from_id == to_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cannot transfer money to the same card'
        )

def check_card_owner(card_owner_id: UUID, current_user_id: UUID):
    if card_owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You can only send money only from and to your own cards'
        )
