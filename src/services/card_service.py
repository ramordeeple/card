from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.card import Card
from src.domain.enums.card_status import CardStatus
from src.domain.rules import card_rules


class CardService:
    @staticmethod
    async def block_card(db: AsyncSession, card_id: UUID, owner_id: UUID):
        query = select(Card).where(Card.id == card_id, Card.owner_id == owner_id)
        result = await db.execute(query)
        card = result.scalar_one_or_none()

        card_rules.check_card_existence(card)
        card_rules.check_card_is_blocked(card)

        card.status = CardStatus.BLOCKED

        await db.commit()
        await db.refresh(card)

        return card

    async def unblock_card(db: AsyncSession, card_id: UUID, owner_id: UUID):
        query = select(Card).where(Card.id == card_id, Card.owner_id == owner_id)
        result = await db.execute(query)
        card = result.scalar_one_or_none()

        card_rules.check_card_existence(card)
        card_rules.check_card_is_active(card)

        card.status = CardStatus.ACTIVE

        await db.commit()
        await db.refresh(card)

        return card
