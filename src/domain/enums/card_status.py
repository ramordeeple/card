from enum import Enum


class CardStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    BLOCKED = 'BLOCKED'
    EXPIRED = 'EXPIRED'