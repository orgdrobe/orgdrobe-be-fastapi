from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import String, DateTime, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import ModelBase

if TYPE_CHECKING:
    from models import (UserIdentity, Role, UserRole, 
                        RefreshToken, Garment, Outfit)

class User(ModelBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text('false'))

    identities: Mapped[list["UserIdentity"]] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan"
    )

    user_roles: Mapped[list["UserRole"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    roles: Mapped[list["Role"]] = relationship(
        secondary="user_roles",
        viewonly=True
    )

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user")

    garments: Mapped[list["Garment"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    outfits: Mapped[list["Outfit"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text('now()'))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text('now()'), onupdate=text('now()'))

    

