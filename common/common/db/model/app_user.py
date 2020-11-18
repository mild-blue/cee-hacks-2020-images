from sqlalchemy import Column, Integer, UniqueConstraint, \
    TEXT, Enum, DateTime, func, PrimaryKeyConstraint  # pylint: disable=import-error

from common.db.base import Base
from common.db.model_utils import get_unique_key_name, get_primary_key_name
from common.enums.app_user_role import AppUserRole


class AppUser(Base):
    """
    App user class
    """
    __tablename__ = "app_users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(TEXT, unique=True, nullable=False)
    pass_hash = Column(TEXT, unique=False, nullable=False)
    role = Column(Enum(AppUserRole), unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    PrimaryKeyConstraint(name=get_primary_key_name(__tablename__))
    UniqueConstraint("username", name=get_unique_key_name(__tablename__, "username"))

    def __init__(
            self,
            username: str,
            pass_hash: str,
            role: AppUserRole
    ) -> None:
        self.username = username
        self.pass_hash = pass_hash
        self.role = role
