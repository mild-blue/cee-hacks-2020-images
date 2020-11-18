from typing import List, Optional, cast
from uuid import UUID

from sqlalchemy import asc
from sqlalchemy.orm import Session  # pylint: disable=import-error

from common.db.database import get_db_session
from common.db.model.job import Job
from common.db.model.job_transition import JobTransition
from common.db.repository.base_repository import BaseRepository
from common.enums.job_status_enum import JobStatusEnum


class JobRepository(BaseRepository):
    """
    Job repository
    """

    @staticmethod
    def get_all() -> List[Job]:
        sup = super(JobRepository, JobRepository)
        return sup.base_get_all(Job)  # type: ignore

    @staticmethod
    def create(job: Job, commit: bool = True) -> Job:
        sup = super(JobRepository, JobRepository)
        return sup.base_create(job, commit)  # type: ignore

    @staticmethod
    def create_many(jobs: List[Job], commit: bool = True) -> List[Job]:
        sup = super(JobRepository, JobRepository)
        sup.base_create_many(jobs, commit)  # type: ignore
        return jobs

    @staticmethod
    def count(session: Optional[Session] = None) -> int:
        session = session if session else get_db_session()
        assert session is not None, "DB must be initialized at this point."
        return session.query(Job).count()  # type: ignore  # pylint: disable=no-member

    @staticmethod
    def get_by_id(idd: UUID) -> Optional[Job]:
        sup = super(JobRepository, JobRepository)
        return sup.base_get_by_id(Job, idd)  # type: ignore

    @staticmethod
    def get_queued_job_to_process() -> Optional[Job]:
        session = BaseRepository.get_session()
        # pylint: disable=E1101,C0301

        subquery_queued = session.query(JobTransition.job_id). \
            filter(JobTransition.status == JobStatusEnum.QUEUED)

        subquery_in_progress = session.query(JobTransition.job_id). \
            filter(JobTransition.status == JobStatusEnum.IN_PROGRESS)

        subquery_finished = session.query(JobTransition.job_id). \
            filter(JobTransition.status == JobStatusEnum.FINISHED)

        subquery_failure = session.query(JobTransition.job_id). \
            filter(JobTransition.status == JobStatusEnum.FAILURE)

        item = session.query(Job).\
            join(Job.transitions).\
            filter(Job.id.in_(subquery_queued)). \
            filter(Job.id.notin_(subquery_in_progress)). \
            filter(Job.id.notin_(subquery_finished)). \
            filter(Job.id.notin_(subquery_failure)). \
            order_by(asc(Job.created_at)).\
            first()  # type: ignore  # noqa: E501
        return cast(Job, item)
