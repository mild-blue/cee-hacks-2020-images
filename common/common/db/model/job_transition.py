from sqlalchemy import Column, Integer, UniqueConstraint, \
    Enum, DateTime, func, ForeignKey, PrimaryKeyConstraint  # pylint: disable=import-error
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import RelationshipProperty, relationship

from common.db.base import Base
from common.db.model.job import Job
from common.db.model_utils import get_unique_key_name, get_foreign_key_name, get_primary_key_name
from common.enums.job_status_enum import JobStatusEnum


class JobTransition(Base):
    """
    JobTransition user class
    """
    __tablename__ = "job_transitions"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    status = Column(Enum(JobStatusEnum), unique=False, nullable=False)
    job_id = Column(
        UUID(as_uuid=True),
        ForeignKey(f"{Job.__tablename__}.id", name=get_foreign_key_name(__tablename__, "job_id")),
        nullable=False
    )
    job: RelationshipProperty = relationship(Job)
    created_at = Column(DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    PrimaryKeyConstraint(name=get_primary_key_name(__tablename__))
    UniqueConstraint("status", "job_id", name=get_unique_key_name(__tablename__, "status_job_id"))

    def __init__(
            self,
            status: JobStatusEnum,
            job: Job
    ) -> None:
        self.status = status
        self.job = job
