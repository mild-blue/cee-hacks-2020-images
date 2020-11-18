from typing import List, Optional, cast
from uuid import UUID

from sqlalchemy import desc
from sqlalchemy.orm import Session  # pylint: disable=import-error

from common.db.database import get_db_session
from common.db.model.job_transition import JobTransition
from common.db.repository.base_repository import BaseRepository


class JobTransitionRepository(BaseRepository):
    """
    JobTransition repository
    """

    @staticmethod
    def get_all() -> List[JobTransition]:
        sup = super(JobTransitionRepository, JobTransitionRepository)
        return sup.base_get_all(JobTransition)  # type: ignore

    @staticmethod
    def create(job_transition: JobTransition, commit: bool = True) -> JobTransition:
        sup = super(JobTransitionRepository, JobTransitionRepository)
        return sup.base_create(job_transition, commit)  # type: ignore

    @staticmethod
    def create_many(job_transitions: List[JobTransition], commit: bool = True) -> List[JobTransition]:
        sup = super(JobTransitionRepository, JobTransitionRepository)
        sup.base_create_many(job_transitions, commit)  # type: ignore
        return job_transitions

    @staticmethod
    def count(session: Optional[Session] = None) -> int:
        session = session if session else get_db_session()
        assert session is not None, "DB must be initialized at this point."
        return session.query(JobTransition).count()  # type: ignore  # pylint: disable=no-member

    @staticmethod
    def get_by_id(idd: int) -> Optional[JobTransition]:
        sup = super(JobTransitionRepository, JobTransitionRepository)
        return sup.base_get_by_id(JobTransition, idd)  # type: ignore

    @staticmethod
    def get_latest_job_transition(job_id: UUID) -> Optional[JobTransition]:
        session = BaseRepository.get_session()
        # pylint: disable=E1101,C0301
        item = session.query(JobTransition).filter(JobTransition.job_id == job_id) \
            .order_by(desc(JobTransition.id)).first()  # type: ignore  # noqa: E501
        return cast(JobTransition, item)
