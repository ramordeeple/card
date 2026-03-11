import bcrypt

encoding: str = 'utf-8'

def hash_password(password: str) -> str:

    pwd_bytes = password.encode(encoding)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)

    return hashed.decode(encoding)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(encoding),
                          hashed_password.encode(encoding))
