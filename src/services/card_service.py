from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from src.core.security.crypto import encrypt_card_number, decrypt_card_number
from src.db.models.card import Card
from src.domain.rules import card_rules
from src.schemas.card import CardCreate


class CardService:
    @staticmethod
    def create_card(db: Session, card_in: CardCreate) -> Card:
        encrypted_bytes = encrypt_card_number(card_in.number)

        new_card = Card(
            owner_id=card_in.owner_id,
            number_encrypted=encrypted_bytes,
            balance=Decimal('0.00')
        )

        db.add(new_card)
        db.commit()
        db.refresh(new_card)

        return new_card

    @staticmethod
    def get_card_for_display(db: Session, card_id: UUID) -> dict:
        card = db.query(Card).filter(Card.id == card_id).first()
        if not card:
            return None

        raw_number = decrypt_card_number(card.number_encrypted)
        masked = card_rules.get_masked_card_number(raw_number)

        return {
            "id": card.id,
            "balance": card.balance,
            "number_masked": masked,
        }