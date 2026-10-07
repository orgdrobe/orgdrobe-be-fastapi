from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import ModelBase

if TYPE_CHECKING:
    from models import User


class UserAvatar(ModelBase):
    __tablename__ = "user_avatars"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    image_key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    user: Mapped["User"] = relationship(back_populates="avatar")
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=text("now()"),
    )

