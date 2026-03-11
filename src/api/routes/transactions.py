from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.api.deps import get_current_user
from src.api.routes.auth import get_db
from src.db.models.card import Card
from src.services.transaction_service import TransactionService

router = APIRouter(prefix="/transactions", tags=["Transactions"])

class TransferRequest(BaseModel):
    from_card_id: UUID
    to_card_id: UUID
    amount: Decimal

@router.post("/transfer", status_code=status.HTTP_200_OK)
def transfer_funds(payload: TransferRequest,
                   db: Session = Depends(get_db),
                   current_user = Depends(get_current_user)
                   ):
    sender_card = db.query(Card).filter(
        Card.id == payload.from_card_id,
        Card.owner_id == current_user.id
    ).first()

    if not sender_card:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You can only transfer funds from your own card")

    return TransactionService.transfer_money(
        db=db,
        from_card_id=payload.from_card_id,
        to_card_id=payload.to_card_id,
        amount=payload.amount,
    )
