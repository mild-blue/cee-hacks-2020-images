import uuid
from typing import Optional

from sqlalchemy import Column, DateTime, func, PrimaryKeyConstraint, Integer, ForeignKey  # pylint: disable=import-error
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import RelationshipProperty, relationship

from common.db.base import Base
from common.db.model.app_user import AppUser
from common.db.model_utils import get_primary_key_name, get_foreign_key_name


class Job(Base):
    """
    Job class
    """
    __tablename__ = "jobs"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=lambda: uuid.uuid4(),  # pylint: disable=W0108
        nullable=False
    )
    app_user_id = Column(
        Integer,
        ForeignKey(f"{AppUser.__tablename__}.id", name=get_foreign_key_name(__tablename__, "app_user_id")),
        nullable=False
    )
    app_user: RelationshipProperty = relationship(AppUser)
    transitions: RelationshipProperty = relationship("JobTransition", back_populates="job")
    created_at = Column(DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    PrimaryKeyConstraint(name=get_primary_key_name(__tablename__))

    def __init__(
            self,
            app_user: AppUser,
            job_id: Optional[UUID] = None
    ) -> None:
        self.app_user = app_user
        self.id = job_id
