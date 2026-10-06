from passlib.context import CryptContext

from core.security.crypto import pwd_context

def get_pwd_context() -> CryptContext:
    """Provide CryptContext instance configured for password hashing."""
    return pwd_context