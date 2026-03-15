import uuid
from typing import List, Optional

from fastapi import APIRouter, status, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.db.models.card import Card
from src.db.models.user import User
from src.db.session import get_db

from src.domain.rules import card_rules
from src.schemas.card import CardRead, CardDeposit, TransferRequest
from src.services.card_service import CardService
from src.services.transaction_service import TransactionService

router = APIRouter(prefix='/cards', tags=['Cards'])

@router.post('/issue', response_model=CardRead, status_code=status.HTTP_201_CREATED)
async def issue_card(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await CardService.issue_card(db, current_user.id)

@router.get('/', response_model=List[CardRead])
async def get_cards(
    search: Optional[str] = Query(None),
    limit: int = 5,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await CardService.get_cards(db, owner_id=user.id, search=search, limit=limit, offset=offset)

@router.post('/transfer', response_model=CardRead)
async def transfer_between_cards(
    payload: TransferRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    card_obj = await TransactionService.transfer_money(
        db, payload.from_id, payload.to_id, payload.amount, owner_id=current_user.id
    )

    return CardRead.model_validate(card_obj)

@router.post('/{card_id}/deposit', response_model=CardRead)
async def deposit_to_card(
    card_id: uuid.UUID,
    payload: CardDeposit,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await TransactionService.deposit(
        db=db, card_id=card_id, amount=payload.amount, owner_id=current_user.id
    )

@router.patch('/{card_id}/block', response_model=CardRead)
async def block_card(
    card_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    card = await CardService.block_card(db, card_id, current_user.id)

    return card

@router.patch('/{card_id}/unblock', response_model=CardRead)
async def unblock_card(
    card_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    card = await CardService.unblock_card(db, card_id, current_user.id)

    return card

@router.get('/{card_id}/balance')
async def get_card_balance(
    card_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    card = await db.get(Card, card_id)

    card_rules.check_card_access(card, current_user.id)

    return {
        'card_id': card.id,
        'balance': card.balance,
    }