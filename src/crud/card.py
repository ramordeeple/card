import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.card import Card


async def get_cards_by_ids(db: AsyncSession, card_ids: list[uuid.UUID], owner_id: uuid.UUID):
    result = await db.execute(
        select(Card).where(
            Card.id.in_(card_ids),
            Card.owner_id == owner_id
        )
    )

    return result.scalars().all()