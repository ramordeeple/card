from decimal import Decimal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from fastapi import HTTPException, status  # Импортируем status
from sqlalchemy.sql import crud

from src.db.models.card import Card


class TransactionService:
    @staticmethod
    async def transfer_money(db: AsyncSession, from_id: UUID, to_id: UUID, amount: Decimal, owner_id: UUID):
        if amount <= Decimal('0.00'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Transaction cannot be negative or equal to zero')

        ids = sorted([from_id, to_id])
        cards = await crud.get_cards(db, ids, owner_id)

        if len(cards) < 2:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cards not found')

        cards_map = {card.id: card for card in cards}
        sender, receiver = cards_map[from_id], cards_map[to_id]

        if sender.balance < amount:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Insufficient funds')

        sender.balance -= amount
        receiver.balance += amount

        return sender