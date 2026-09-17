from typing import Optional, TYPE_CHECKING
from datetime import datetime

from sqlalchemy import String, Text, ForeignKey, DateTime, text, Boolean
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import ModelBase

if TYPE_CHECKING:
    from models import (User, Color, Garment)

class Outfit(ModelBase):
    __tablename__ = "outfits"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="outfits")

    outfit_garments: Mapped[list["OutfitGarment"]] = relationship(back_populates="outfit", cascade="all, delete-orphan")
    garments: Mapped[list["Garment"]] = relationship(secondary="outfit_garments", viewonly=True)

    outfit_colors: Mapped[list["OutfitColor"]] = relationship(back_populates="outfit", cascade="all, delete-orphan")
    colors: Mapped[list["Color"]] = relationship(secondary="outfit_colors", viewonly=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text('now()'))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text('now()'), onupdate=text('now()'))


class OutfitGarment(ModelBase):
    __tablename__ = "outfit_garments"

    outfit_id: Mapped[int] = mapped_column(ForeignKey("outfits.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    garment_id: Mapped[int] = mapped_column(ForeignKey("garments.id", ondelete="CASCADE"), nullable=False, primary_key=True)

    outfit: Mapped["Color"] = relationship(back_populates="outfit_garments")
    garment: Mapped["Garment"] = relationship(back_populates="garment_outfits")


class OutfitColor(ModelBase):
    __tablename__ = "outfit_colors"

    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False)

    color_id: Mapped[int] = mapped_column(ForeignKey("colors.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    outfit_id: Mapped[int] = mapped_column(ForeignKey("outfits.id", ondelete="CASCADE"), nullable=False, primary_key=True)

    color: Mapped["Color"] = relationship(back_populates="color_outfits")
    outfit: Mapped["Outfit"] = relationship(back_populates="garment_colors")