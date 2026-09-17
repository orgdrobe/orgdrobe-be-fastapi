from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import ModelBase

if TYPE_CHECKING:
    from models.user import User

class Role(ModelBase):
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    role_users: Mapped[list["UserRole"]] = relationship(back_populates="role", cascade="all, delete-orphan")
    users: Mapped[list["User"]] = relationship(secondary="user_roles", viewonly=True)


class UserRole(ModelBase):
    __tablename__ = "user_roles"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), nullable=False, primary_key=True)

    user: Mapped["User"] = relationship(back_populates="user_roles")
    role: Mapped["Role"] = relationship(back_populates="role_users")