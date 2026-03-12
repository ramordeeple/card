import random

from src.domain.constants.card_constants import CARD_NUMBER_LENGTH


def generate_rand_card_number() -> str:
    card_number = ""
    for _ in range(CARD_NUMBER_LENGTH):
        digit = random.randint(0, 9)
        card_number += str(digit)

    return card_number