import hashlib
import hmac
import os

HASH_ALGORITHM = "sha256"
ITERATIONS = 500_000
SALT_SIZE = 16


def generate_salt():
    return os.urandom(SALT_SIZE).hex()


def hash_password(password, salt):
    digest = hashlib.pbkdf2_hmac(HASH_ALGORITHM, password.encode(), bytes.fromhex(salt), ITERATIONS)
    return digest.hex()


def check_password(password, salt, password_hash):
    return hmac.compare_digest(hash_password(password, salt), password_hash)
