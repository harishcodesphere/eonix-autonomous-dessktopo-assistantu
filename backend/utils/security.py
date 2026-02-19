"""
Eonix Security Utilities
Encryption, hashing, and token management.
"""
import hashlib
import secrets
import base64
from cryptography.fernet import Fernet


def generate_secret_key() -> str:
    """Generate a cryptographic secret key."""
    return secrets.token_hex(32)


def generate_encryption_key() -> bytes:
    """Generate a Fernet encryption key."""
    return Fernet.generate_key()


def encrypt_data(data: str, key: bytes) -> str:
    """Encrypt a string using Fernet symmetric encryption."""
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()


def decrypt_data(encrypted: str, key: bytes) -> str:
    """Decrypt a Fernet-encrypted string."""
    f = Fernet(key)
    return f.decrypt(encrypted.encode()).decode()


def hash_string(value: str) -> str:
    """Create a SHA-256 hash of a string."""
    return hashlib.sha256(value.encode()).hexdigest()


def generate_token(length: int = 32) -> str:
    """Generate a URL-safe random token."""
    return secrets.token_urlsafe(length)
