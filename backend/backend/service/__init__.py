from uuid import UUID

from common.db.model.job import Job
from common.db.repository.job_repository import JobRepository


def get_and_guard_job(user_id: int, job_id: UUID) -> Job:
    job = JobRepository.get_by_id(job_id)
    if not job:
        # TODO use custom exceptions for 404
        raise KeyError(f'Job with id {job_id} does not exist!')

    if job.app_user_id != user_id:
        # TODO custom exception
        raise Exception(f'User {user_id} does not have access to the job {job_id}!')
    return job
