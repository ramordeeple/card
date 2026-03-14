from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from src.crud.card import get_cards
from src.db.models.card import Card
from src.domain.rules import card_rules


class TransactionService:
    @staticmethod
    async def transfer_money(db: AsyncSession, from_id: UUID, to_id: UUID, amount: Decimal, owner_id: UUID):
        card_rules.validate_transaction_amount(amount)

        ids = sorted([from_id, to_id])
        cards = await get_cards(db, ids, owner_id)

        if len(cards) < 2:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cards not found')

        cards_map = {card.id: card for card in cards}
        sender, receiver = cards_map[from_id], cards_map[to_id]

        if sender.balance < amount:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Insufficient funds')

        sender.balance -= amount
        receiver.balance += amount

        await db.commit()
        await db.refresh(sender)

        return sender

    @staticmethod
    async def deposit(
            db: AsyncSession,
            card_id: UUID,
            amount: Decimal,
            owner_id: UUID,
    ):
        card_rules.validate_transaction_amount(amount)
        query = (
            select(Card)
            .where(Card.id == card_id, Card.owner_id == owner_id)
            .with_for_update()
        )
        result = await db.execute(query)
        card = result.scalar_one_or_none()

        if card is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Card not found')

        card.balance += amount

        await db.commit()
        return card