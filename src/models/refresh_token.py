from uuid import UUID
from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import String, DateTime, Boolean, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from .base import ModelBase

if TYPE_CHECKING:
    from models.user import User 

class RefreshToken(ModelBase):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    jti: Mapped[UUID] = mapped_column(Uuid, unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, server_default=text('false'))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text('now()'))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")