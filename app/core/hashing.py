import binascii
import hashlib
import hmac
import os

HASH_NAME = "sha256"
ITERATIONS = 200_000
SALT_SIZE = 16


def hash_password(user_password: str) -> str:
    salt: bytes = os.urandom(SALT_SIZE)

    dk: bytes = hashlib.pbkdf2_hmac(
        hash_name = HASH_NAME, password = user_password.encode(
        encoding = "utf-8"),
        salt = salt, iterations = ITERATIONS
    )

    salt_hex: str = binascii.hexlify(data = salt).decode()
    dk_hex: str = binascii.hexlify(data = dk).decode()

    return (
        f"{HASH_NAME}$"
        f"{ITERATIONS}$"
        f"{salt_hex}$"
        f"{dk_hex}"
    )

def compare_hash_password(stored: str, user_password: str) -> bool:
    hash_name, iters, salt_hex, dk_hex = stored.split(sep = "$")

    salt: bytes = binascii.unhexlify(salt_hex)
    expected: bytes = binascii.unhexlify(dk_hex)

    dk: bytes = hashlib.pbkdf2_hmac(
        hash_name = hash_name,
        password = user_password.encode(encoding = "utf-8"),
        salt = salt,
        iterations = int(iters)
    )

    return hmac.compare_digest(dk, expected)