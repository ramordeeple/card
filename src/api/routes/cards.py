import uuid
from datetime import timedelta, datetime
from decimal import Decimal
from typing import List

from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import deps
from src.api.deps import get_current_user
from src.core.security.crypto import encrypt_card_number
from src.core.util.card_number_generator import generate_rand_card_number
from src.db.models.card import Card
from src.db.models.user import User
from src.db.session import get_db
from src.domain.constants.card_constants import (
    CARD_VALIDITY_YEARS,
    CARD_MASK_VISIBLE_END,
)
from src.domain.enums.card_status import CardStatus
from src.schemas.card import CardRead, CardDeposit, TransferRequest
from src.services.card_service import CardService
from src.services.transaction_service import TransactionService

router = APIRouter(prefix="/cards", tags=["Cards"])


@router.post("/issue", response_model=CardRead, status_code=status.HTTP_201_CREATED)
async def issue_card(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
):
    generated_number = generate_rand_card_number()
    encrypted_bytes = encrypt_card_number(generated_number)

    new_card = Card(
        id=uuid.uuid4(),
        number_encrypted=encrypted_bytes,
        number_last4=generated_number[-CARD_MASK_VISIBLE_END:],
        owner_id=current_user.id,
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


@router.get("/", response_model=List[CardRead])
async def get_cards(
    limit: int = 5,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        select(Card).where(Card.owner_id == current_user.id).limit(limit).offset(offset)
    )

    result = await db.execute(query)
    cards = result.scalars().all()

    return cards


@router.post('/transfer', response_model=CardRead)
async def transfer_between_cards(
    payload: TransferRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    card_obj = await TransactionService.transfer_money(
        db, payload.from_id, payload.to_id, payload.amount, current_user.id
    )

    return CardRead.model_validate(card_obj)


@router.post("/{card_id}/deposit", response_model=CardRead)
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