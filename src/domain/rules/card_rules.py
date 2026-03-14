from decimal import Decimal

def validate_transaction_amount(amount: Decimal) -> None:
    if amount <= Decimal('0.00'):
        raise ValueError('Amount must be positive')