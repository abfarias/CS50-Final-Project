"""
Security module for SafePass

This module contains functions that utilize the argon2-cffi and the cryptography libraries

argon2-cffi: https://argon2-cffi.readthedocs.io/en/stable/argon2.html
cryptography: https://cryptography.io/en/latest/

"""
import base64
from argon2 import PasswordHasher, exceptions
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


ph = PasswordHasher()


def generate_hash(password: str) -> str:
    """Create argon2 hash using default parameters"""
    return ph.hash(password)


def check_password(hash: str, password: str) -> bool:
    """Check if provided password matches hash"""
    try:
        ph.verify(hash, password)
        return True
    except exceptions.VerifyMismatchError:
        return False
    

def check_rehash(hash: str) -> bool:
    """Check if hash parameters are outdated"""
    if ph.check_needs_rehash(hash):
        return True
    return False


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a secure key for encryption"""
    
    password = password.encode('utf-8')

    # Key derivation function setup
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=600000,
    )

    # Key to realize encryption
    key = base64.urlsafe_b64encode(kdf.derive(password))

    return key


def encrypt(key: Fernet, data: str) -> bytes:
    """Encrypt data with Fernet key"""
    data = data.encode('utf-8')
    token = key.encrypt(data)
    return token


def decrypt(key: Fernet, token: bytes) -> bytes:
        """Decrypt data with Fernet key"""
        data = key.decrypt(token)
        return data 
