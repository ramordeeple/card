import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security.crypto import encrypt_card_number
from src.core.util.card_number_generator import generate_rand_card_number
from src.db.models.card import Card
from src.domain.constants.card_constants import (
    CARD_MASK_VISIBLE_END,
    CARD_VALIDITY_YEARS,
)
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

    @staticmethod
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

    @staticmethod
    async def issue_card(db: AsyncSession, owner_id: uuid.UUID):
        generated_number = generate_rand_card_number()
        encrypted_bytes = encrypt_card_number(generated_number)

        new_card = Card(
            id=uuid.uuid4(),
            number_encrypted=encrypted_bytes,
            number_last4=generated_number[-CARD_MASK_VISIBLE_END:],
            owner_id=owner_id,
            expiration_date=(
                datetime.now() + timedelta(days=365 * CARD_VALIDITY_YEARS)
            ).date(),
            status=CardStatus.ACTIVE,
            balance=Decimal("0.00"),
        )

        db.add(new_card)
        await db.commit()
        await db.refresh(new_card)

        return new_card

    @staticmethod
    async def get_cards(
        db: AsyncSession,
        owner_id: uuid.UUID | None = None,
        search: str | None = None,
        limit: int = 10,
        offset: int = 0,
    ):
        query = select(Card)

        if owner_id:
            query = query.where(Card.owner_id == owner_id)

        if search:
            query = query.where(Card.number_last4.contains(search))

        count_query = select(func.count()).select_from(query.subquery())
        total = await db.scalar(count_query)

        result = await db.execute(query.limit(limit).offset(offset))
        cards = result.scalars().all()

        return {
            'items': cards,
            'total': total or 0,
            'limit': limit,
            'offset': offset,
        }