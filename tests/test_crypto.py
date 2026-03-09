from src.core.security.crypto import encrypt_card_number, decrypt_card_number


def test_encrypt_decrypt_cycle():
    raw_number = "1234567812345678"
    encrypted_bytes = encrypt_card_number(raw_number)

    assert isinstance(encrypted_bytes, bytes)

    decrypted_number = decrypt_card_number(encrypted_bytes)

    assert decrypted_number == raw_number

def test_randomization():
    raw_number = "1234567812345678"

    res1 = encrypt_card_number(raw_number)
    res2 = encrypt_card_number(raw_number)

    assert res1 != res2