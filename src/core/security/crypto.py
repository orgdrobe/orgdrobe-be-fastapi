from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["argon2"],
    argon2__memory_cost=65536,
    argon2__time_cost=3,
)