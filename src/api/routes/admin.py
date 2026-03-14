from uuid import UUID

from fastapi import Query, APIRouter
from fastapi.params import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.card import Card
from src.db.models.user import User
from src.db.session import get_db
from src.domain.enums.card_status import CardStatus
from src.domain.rules import card_rules

router = APIRouter(prefix='/admin', tags=['Admin Operations'])

@router.get('/cards')
async def get_all_cards(
        db: AsyncSession = Depends(get_db),
        limit: int = Query(10, ge=1, le=100, alias='limit'),
        offset: int = Query(0, ge=0)
):
    statement = select(Card).limit(limit).offset(offset)
    result = await db.execute(statement)
    cards = result.scalars().all()

    total_result = await db.execute(select(func.count(Card.id)))

    return {
        'items': cards,
        'total': total_result,
        'offset': offset,
        'limit': limit
    }


@router.get('/users')
async def get_all_users(
        db: AsyncSession = Depends(get_db),
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0)
):
    statement = select(User).limit(limit).offset(offset)
    result = await db.execute(statement)
    users = result.scalars().all()

    total_result = await db.execute(select(func.count(User.id)))
    total = total_result.scalars()

    return {
        'items': users,
        'limit': limit,
        'offset': offset,
        'total': total
    }

@router.patch('/cards/{card_id}/unblock')
async def admin_unblock_card(
        card_id: UUID,
        db: AsyncSession = Depends(get_db),
):
    statement = select(User).where(User.id == card_id)
    result = await db.execute(statement)
    card = result.scalar_one_or_none()

    card_rules.check_card_existence(card)
    card_rules.check_card_is_active(card)

    card.status = CardStatus.ACTIVE

    await db.commit()
    await db.refresh(card)

    return {
        'message': f'Card {card_id} unblocked successfully',
        'status': card.status
    }

@router.patch('/cards/{card_id}/block')
async def admin_block_card(
        card_id: UUID,
        db: AsyncSession = Depends(get_db),
):
    statement = select(User).where(User.id == card_id)
    result = await db.execute(statement)
    card = result.scalar_one_or_none()

    card_rules.check_card_existence(card)
    card_rules.check_card_is_active(card)

    card.status = CardStatus.BLOCKED

    await db.commit()
    await db.refresh(card)

    return {
        'message': f'Card {card_id} unblocked successfully',
        'status': card.status
    }