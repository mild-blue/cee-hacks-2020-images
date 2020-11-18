from typing import Optional
from uuid import UUID

from common.db.model.job import Job
from common.db.model.job_transition import JobTransition
from common.db.repository.app_user_repository import AppUserRepository
from common.db.repository.job_repository import JobRepository
from common.db.repository.job_transition_repository import JobTransitionRepository
from common.enums.job_status_enum import JobStatusEnum, ALLOWED_JOB_STATUS_TRANSITIONS
from common.exceptions import InvalidArgumentException


class JobService:
    @staticmethod
    def create_job(app_user_id: int) -> Job:
        """
        Created new job with initial QUEUED status in transition.
        :param app_user_id:
        :return:
        """
        app_user = AppUserRepository.get_by_id(app_user_id)
        if app_user is None:
            raise InvalidArgumentException(f"App user {app_user_id} does not exist.")

        job = JobRepository.create(Job(app_user), False)
        JobTransitionRepository.create(JobTransition(JobStatusEnum.INITIAL, job), False)
        # pylint: disable=E1101
        JobTransitionRepository.get_session().commit()  # type: ignore
        return job

    @staticmethod
    def add_job_status(job_id: UUID, status: JobStatusEnum) -> JobTransition:
        """
        Add new to status to Job.
        :param job_id:
        :param status:
        :return:
        """
        job = JobRepository.get_by_id(job_id)
        if job is None:
            raise InvalidArgumentException(f"Job {job_id} does not exist.")

        job_transition = sorted(job.transitions, key=lambda transition: transition.id, reverse=True)[0]  # type: ignore
        if status not in ALLOWED_JOB_STATUS_TRANSITIONS.get(job_transition.status, {}):
            raise InvalidArgumentException(f"Invalid transition from status {job_transition.status} to {status}.")

        return JobTransitionRepository.create(JobTransition(status, job))

    @staticmethod
    def get_queued_job_to_process_and_set_it_to_in_progress() -> Optional[Job]:
        """
        Gets the oldest QUEUED job to be processed and set its status to IN_PROGRESS if such job exists.
        Otherwise returns null.
        :return:
        """
        session = JobRepository.get_session()
        session.execute(f'LOCK TABLE {JobTransition.__tablename__} IN ACCESS EXCLUSIVE MODE;')
        job = JobRepository.get_queued_job_to_process()
        if job is None:
            return None
        JobService.add_job_status(job.id, JobStatusEnum.IN_PROGRESS)
        session.commit()
        return job
