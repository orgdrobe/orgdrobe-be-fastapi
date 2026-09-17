from typing import TYPE_CHECKING,Optional

from sqlalchemy import String, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import ModelBase
from core.enums.auth_providers import AuthProvider

if TYPE_CHECKING:
    from models import User

class UserIdentity(ModelBase):
    __tablename__ = "user_identities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    provider: Mapped[AuthProvider] = mapped_column(Enum(AuthProvider, name="auth_provider_enum", native_enum=True), nullable=False)
    provider_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False) # email for local, sub_id for google
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    user: Mapped["User"] = relationship(back_populates="identities")


    
    
   

