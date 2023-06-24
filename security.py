"""
Security module for SafePass

For now this module contains three functions that utilize the argon2-cffi library

argon2-cffi: https://argon2-cffi.readthedocs.io/en/stable/argon2.html

"""

from argon2 import PasswordHasher, exceptions

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
