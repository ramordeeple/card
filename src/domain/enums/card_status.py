from enum import Enum


class CardStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    EXPIRED = 'EXPIRED'