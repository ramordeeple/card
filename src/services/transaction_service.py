from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.card import Card
from src.domain.rules import card_rules, transaction_rules
from src.domain.rules.card_rules import check_card_existence


class TransactionService:
    @staticmethod
    async def transfer_money(db: AsyncSession, from_id: UUID, to_id: UUID, amount: Decimal, owner_id: UUID):
        card_rules.validate_transaction_amount(amount)

        ids = sorted([from_id, to_id])

        statement = select(Card).where(Card.id.in_(ids)).with_for_update()
        result = await db.execute(statement)
        cards = result.scalars().all()

        transaction_rules.check_not_same_card(from_id, to_id)
        transaction_rules.check_both_cards_found(cards)

        cards_map = {card.id: card for card in cards}
        sender, receiver = cards_map[from_id], cards_map[to_id]

        for card in cards:
            transaction_rules.check_card_owner(card.owner_id, owner_id)

        card_rules.check_card_is_active(sender, card_name="Sender card")
        card_rules.check_card_is_active(receiver, card_name="Receiver card")

        transaction_rules.check_sufficient_funds(sender.balance, amount)

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

        check_card_existence(card)

        card.balance += amount

        await db.commit()
        return card