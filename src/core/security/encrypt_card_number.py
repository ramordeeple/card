import base64
import os
from typing import Final
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from src.core.config import settings

AES_KEY_SIZE: Final[int] = 32
AES_IV_SIZE: Final[int] = 12

def _get_cipher() -> AESGCM:
    key_bytes = base64.b64decode(settings.ENCRYPTION_KEY)

    return AESGCM(key_bytes[:AES_KEY_SIZE])

def encrypt_card_number(plain_number:str) -> bytes:
    cipher = _get_cipher()
    iv = os.urandom(AES_IV_SIZE)
    encrypted_payload = cipher.encrypt(iv, plain_number.encode(), None)

    return iv + encrypted_payload

def decrypt_card_number(combined_bytes: bytes) -> str:
    cipher = _get_cipher()

    iv = combined_bytes[:AES_IV_SIZE]
    ciphertext = combined_bytes[AES_IV_SIZE:]
    decrypted_bytes = cipher.decrypt(iv, ciphertext, None)

    return decrypted_bytes.decode()