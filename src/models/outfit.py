from typing import Optional, TYPE_CHECKING
from datetime import datetime

from sqlalchemy import String, Text, ForeignKey, DateTime, text, Boolean, Table, Column, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import ModelBase

if TYPE_CHECKING:
    from models import (User, Color, Garment)

outfit_garments = Table(
    "outfit_garments",
    ModelBase.metadata,
    Column("outfit_id", ForeignKey("outfits.id", ondelete="CASCADE"), primary_key=True),
    Column("garment_id", ForeignKey("garments.id", ondelete="CASCADE"), primary_key=True),
)


class Outfit(ModelBase):
    __tablename__ = "outfits"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="outfits")

    garments: Mapped[list["Garment"]] = relationship(
        secondary=outfit_garments,
        back_populates="outfits",
        lazy="selectin",
    )

    colors: Mapped[list["OutfitColor"]] = relationship(
        back_populates="outfit",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    images: Mapped[list["OutfitImage"]] = relationship(
        back_populates="outfit",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="OutfitImage.order",
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text('now()'))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text('now()'), onupdate=text('now()'))


class OutfitImage(ModelBase):
    __tablename__ = "outfit_images"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    image_key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    outfit_id: Mapped[int] = mapped_column(
        ForeignKey("outfits.id", ondelete="CASCADE"), nullable=False, index=True
    )
    outfit: Mapped["Outfit"] = relationship(back_populates="images")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )


class OutfitColor(ModelBase):
    __tablename__ = "outfit_colors"

    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False)

    color_id: Mapped[int] = mapped_column(ForeignKey("colors.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    outfit_id: Mapped[int] = mapped_column(ForeignKey("outfits.id", ondelete="CASCADE"), nullable=False, primary_key=True)

    color: Mapped["Color"] = relationship(back_populates="color_outfits", lazy="selectin")
    outfit: Mapped["Outfit"] = relationship(back_populates="colors")