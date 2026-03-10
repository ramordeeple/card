from decimal import Decimal
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status  # Импортируем status

from src.db.models.card import Card


class TransactionService:
    @staticmethod
    def transfer_money(
        db: Session, from_card_id: UUID, to_card_id: UUID, amount: Decimal
    ):
        if amount <= Decimal('0.00'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Сумма перевода должна быть положительной',
            )

        try:
            # For avoiding deadlocks
            ids = sorted([from_card_id, to_card_id])

            cards_query = (
                db.query(Card).filter(Card.id.in_(ids)).with_for_update().all()
            )
            cards_map = {card.id: card for card in cards_query}

            if len(cards_map) < 2:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Sender's card or receiver's not found",
                )

            sender = cards_map[from_card_id]
            receiver = cards_map[to_card_id]

            if sender.balance < amount:
                raise HTTPException(
                    status_code=status.HTTP_402_PAYMENT_REQUIRED,
                    detail='Insufficient funds',
                )

            sender.balance -= amount
            receiver.balance += amount

            db.commit()
            return {'status': 'success', 'amount': amount}

        except Exception as e:
            db.rollback()
            if isinstance(e, HTTPException):
                raise e
            # Вместо 500
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Internal Server Error',
            )
