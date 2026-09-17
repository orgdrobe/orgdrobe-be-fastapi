from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, text, CheckConstraint
from sqlalchemy.orm import Mapped
from pgvector.sqlalchemy import Vector

from .database import Base

# SQLAlchemy Models (Database Tables)

# TODO add validation like in Pydantic Models (schemas.py) (a nullable field with minimum length: `name: str | None = Field(default=None,  min_length=1)`)??? nah, too much code

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    login = Column(String, index=True, unique=True, nullable=False) # username
    email = Column(String, index=True, unique=True, nullable=False) 
    password = Column(String, nullable=False)
    
    name = Column(String) # delete
    image_link: Column[str] = Column(String) # avatar
    image_id: Column[int] = Column(Integer, ForeignKey("images_info.id")) # pending

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=lambda: datetime.now(timezone.utc))


class Garment(Base):
    __tablename__ = "garments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True) # назва чисто користувач задає
    description = Column(String) # задає користувач задає
    image_link: Column[str] = Column(String) # це понятно
    hex = Column(String(7)) # main color
    last_worn: Mapped[Optional[datetime]] # delete

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    image_id = Column(Integer, ForeignKey("images_info.id")) # delete

    gender_id = Column(Integer, ForeignKey("genders.id"))
    category_master_id = Column(Integer, ForeignKey("categories_master.id"))
    category_sub_id = Column(Integer, ForeignKey("categories_sub.id"))
    garment_type_id = Column(Integer, ForeignKey("garment_types.id"))
    color_id = Column(Integer, ForeignKey("colors.id")) # because of the dataset
    season_id = Column(Integer, ForeignKey("seasons.id"))
    usage_id = Column(Integer, ForeignKey("uses.id"))
    
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=lambda: datetime.now(timezone.utc))
    
    __table_args__ = (
        CheckConstraint("hex ~ '^#[0-9A-Fa-f]{6}$'", name="hex_regex"),
    )

class Outfit(Base): # colletion 
    __tablename__ = "outfits" # метадані

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True) # назва 
    description = Column(String)
    image_link: Column[str] = Column(String)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    image_id: Column[int] = Column(Integer, ForeignKey("images_info.id")) # загальний образ
    
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=lambda: datetime.now(timezone.utc))

class OutfitGarment(Base):
    __tablename__ = "outfit_garments"
    
    outfit_id = Column(Integer, ForeignKey('outfits.id'), primary_key=True, nullable=False)
    garment_id = Column(Integer, ForeignKey('garments.id'), primary_key=True, nullable=False)

    order = Column(Integer, default=0) # порядок 
    notes = Column(String) # delete

    added_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class ImageInfo(Base):
    __tablename__ = "images_info"
    
    id = Column(Integer, primary_key=True, index=True)

    filename_store = Column(String, nullable=False)
    filename_original = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=lambda: datetime.now(timezone.utc))


class Gender(Base):
    __tablename__ = "genders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=lambda: datetime.now(timezone.utc))

class CategoryMaster(Base):
    __tablename__ = "categories_master"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=lambda: datetime.now(timezone.utc))

class CategorySub(Base):
    __tablename__ = "categories_sub"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=lambda: datetime.now(timezone.utc))

class GarmentType(Base):
    __tablename__ = "garment_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=lambda: datetime.now(timezone.utc))

class Color(Base): # because of dataset
    __tablename__ = "colors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    hex = Column(String(7))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=lambda: datetime.now(timezone.utc))
    __table_args__ = (
        CheckConstraint("hex ~ '^#[0-9A-Fa-f]{6}$'", name="hex_regex"),
    )

class Season(Base):
    __tablename__ = "seasons"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=lambda: datetime.now(timezone.utc))

class Usage(Base):
    __tablename__ = "uses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=lambda: datetime.now(timezone.utc))


class MLMapping(Base):
    __tablename__ = "ml_mappings"
    
    id = Column(Integer, primary_key=True, index=True)
    ml_category_id = Column(Integer, nullable=False)
    ml_category_name = Column(String, nullable=False)
    # model_id = Column(Integer, ForeignKey('ml_models.id'), primary_key=True) #TODO when i wll be adding new models
    
    # each row only uses one FK because im too lasy to create a bunch of tables for each thing
    gender_id = Column(Integer, ForeignKey("genders.id"), nullable=True)
    category_master_id = Column(Integer, ForeignKey("categories_master.id"), nullable=True)
    category_sub_id = Column(Integer, ForeignKey("categories_sub.id"), nullable=True)
    garment_type_id = Column(Integer, ForeignKey("garment_types.id"), nullable=True)
    color_id = Column(Integer, ForeignKey("colors.id"), nullable=True)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=True)
    usage_id = Column(Integer, ForeignKey("uses.id"), nullable=True)
    
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class OutfitTemplate(Base):
    __tablename__ = "outfit_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=lambda: datetime.now(timezone.utc))

class OutfitTemplateParameter(Base):
    __tablename__ = "outfit_template_parameters"

    outfit_template_id = Column(Integer, ForeignKey("outfit_templates.id"), primary_key=True, nullable=False)
    category_sub_id = Column(Integer, ForeignKey("categories_sub.id"), primary_key=True, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class GarmentEmbeddings(Base):
    __tablename__ = "garment_embeddings"
    garment_id = Column(Integer, ForeignKey('garments.id'), primary_key=True, nullable=False)

    # model_id = Column(Integer, ForeignKey('ml_models.id'), primary_key=True) #TODO when i wll be adding new models
    embedding_image = Column(Vector) 
    embedding_metadata = Column(Vector) 
    embedding_combined = Column(Vector)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=lambda: datetime.now(timezone.utc))

#TODO when there will be more models
# class MLModel(Base):
#     __tablename__ = "ml_models"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     description = Column(String) #with path and filename (or add these as fields)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
#     updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=lambda: datetime.now(timezone.utc))