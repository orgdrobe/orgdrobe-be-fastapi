from core.security.crypto import pwd_context

def test_password_hashing():
    hashed = pwd_context.hash("secret123")
    assert pwd_context.verify("secret123", hashed)
    assert not pwd_context.verify("wrong_password", hashed)