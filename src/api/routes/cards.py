import uuid
from datetime import timedelta, datetime
from decimal import Decimal

from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import deps
from src.core.util.card_number_generator import generate_rand_card_number
from src.db.models.card import Card
from src.db.models.user import User
from src.db.session import SessionLocal
from src.domain.constants.card_constants import CARD_VALIDITY_YEARS
from src.domain.enums.card_status import CardStatus
from src.schemas.card import CardRead

router = APIRouter(prefix='/cards', tags=['Cards'])

@router.post('/issue', response_model=CardRead, status_code=status.HTTP_201_CREATED)
async def issue_card(
        db: AsyncSession = Depends(SessionLocal), #TODO
        current_user: User = Depends(deps.get_current_user)
):
    new_card = Card(
        id=uuid.uuid4(),
        number_encrypted=generate_rand_card_number(),
        owner_id=current_user.id,
        expiration_date=(datetime.now() + timedelta(days=365 * CARD_VALIDITY_YEARS)).date(),
        status=CardStatus.ACTIVE,
        balance=Decimal('0.00')
    )

    db.add(new_card)
    await db.commit()
    await db.refresh(new_card)

    return new_card