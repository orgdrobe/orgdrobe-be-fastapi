from typing import Optional, TYPE_CHECKING
from datetime import datetime

from sqlalchemy import String, Text, ForeignKey, DateTime, text, Boolean
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import ModelBase

if TYPE_CHECKING:
    from models import (User, Gender, CategoryMaster, 
                        CategorySub, GarmentType, Season,
                        Usage, Color, Outfit)

class Garment(ModelBase):
    __tablename__ = "garments"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="garments")

    gender_id: Mapped[int] = mapped_column(ForeignKey("genders.id", ondelete="RESTRICT"), nullable=False)
    gender: Mapped["Gender"] = relationship(back_populates="garments", lazy="selectin")

    category_master_id: Mapped[int] = mapped_column(ForeignKey("categories_master.id", ondelete="RESTRICT"), nullable=False)
    category_master: Mapped["CategoryMaster"] = relationship(back_populates="garments", lazy="selectin")

    category_sub_id: Mapped[int] = mapped_column(ForeignKey("categories_sub.id", ondelete="RESTRICT"), nullable=False)
    category_sub: Mapped["CategorySub"] = relationship(back_populates="garments", lazy="selectin")

    garment_type_id: Mapped[int] = mapped_column(ForeignKey("garment_types.id", ondelete="RESTRICT"), nullable=False)
    garment_type: Mapped["GarmentType"] = relationship(back_populates="garments", lazy="selectin")

    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id", ondelete="RESTRICT"), nullable=False)
    season: Mapped["Season"] = relationship(back_populates="garments", lazy="selectin")

    usage_id: Mapped[int] = mapped_column(ForeignKey("uses.id", ondelete="RESTRICT"), nullable=False)
    usage: Mapped["Usage"] = relationship(back_populates="garments", lazy="selectin")

    colors: Mapped[list["GarmentColor"]] = relationship(back_populates="garment", cascade="all, delete-orphan", lazy="selectin")

    outfits: Mapped[list["Outfit"]] = relationship(
        secondary="outfit_garments",
        back_populates="garments",
        lazy="selectin"
    )
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text('now()'))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text('now()'), onupdate=text('now()'))


class GarmentColor(ModelBase):
    __tablename__ = "garment_colors"

    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False)

    color_id: Mapped[int] = mapped_column(ForeignKey("colors.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    garment_id: Mapped[int] = mapped_column(ForeignKey("garments.id", ondelete="CASCADE"), nullable=False, primary_key=True)

    color: Mapped["Color"] = relationship(back_populates="color_garments", lazy="selectin")
    garment: Mapped["Garment"] = relationship(back_populates="colors")
