"""
Security module for SafePass

This module contains functions that utilize the argon2-cffi and the cryptography libraries

argon2-cffi: https://argon2-cffi.readthedocs.io/en/stable/argon2.html
cryptography: https://cryptography.io/en/latest/

"""

import os
from argon2 import PasswordHasher, exceptions
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


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


def generate_user_public_key():
    """Generate random AES-GCM key"""
    key = AESGCM.generate_key(bit_length=128)
    return AESGCM(key)


def encrypt_data(data: str, user_public_key: AESGCM, user_secret_key: str) -> tuple[bytes, bytes]:
    """Encrypt provided data"""

    # Convert strings to binary
    binary_data = data.encode('utf-8')
    user_secret_key = user_secret_key.encode('utf-8')
    
    # Set up random bytenumber
    nonce = os.urandom(16)

    # Call encrypt method
    encrypted_data = user_public_key.encrypt(nonce, binary_data, user_secret_key)
    
    # Return resulting encrypted data and random bytenumber
    return encrypted_data, nonce


def decrypt_data(*encrypted_data, user_public_key: AESGCM, user_secret_key: str) -> str:
    """Decrypt provided data"""

    # Convert string to binary
    user_secret_key = user_secret_key.encode('utf-8')
    
    # Call decrypt method
    decrypted_data = user_public_key.decrypt(encrypted_data[1], encrypted_data[0], user_secret_key)
    
    # Return decrypted data as string 
    return decrypted_data.decode('utf-8')
