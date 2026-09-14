from typing import Optional, TYPE_CHECKING
from datetime import datetime

from sqlalchemy import String, Text, DateTime, text
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import ModelBase

if TYPE_CHECKING:
    from models import Garment

class CategoryMaster(ModelBase):
    __tablename__ = "categories_master"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    garments: Mapped[list["Garment"]] = relationship(back_populates="category_master")
   
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text('now()'))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text('now()'), onupdate=text('now()'))