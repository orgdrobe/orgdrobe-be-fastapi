from typing import TYPE_CHECKING

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import ModelBase

if TYPE_CHECKING:
    from models import Garment, GarmentColor, OutfitColor, Outfit

class Color(ModelBase):
    __tablename__ = "colors"
    id: Mapped[int] = mapped_column(primary_key=True)

    red: Mapped[int] = mapped_column(Integer, nullable=False)
    green: Mapped[int] = mapped_column(Integer, nullable=False)
    blue: Mapped[int] = mapped_column(Integer, nullable=False)

    color_garments: Mapped[list["GarmentColor"]] = relationship(back_populates="color", cascade="all, delete-orphan")
    garments: Mapped[list["Garment"]] = relationship(secondary="garment_colors", viewonly=True)

    color_outfits: Mapped[list["OutfitColor"]] = relationship(back_populates="color", cascade="all, delete-orphan")
    outfits: Mapped[list["Outfit"]] = relationship(secondary="outfit_colors", viewonly=True)
