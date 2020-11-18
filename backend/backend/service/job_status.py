from uuid import UUID

from backend.service import get_and_guard_job
from common.db.repository.job_transition_repository import JobTransitionRepository
from common.enums.job_status_enum import JobStatusEnum


def get_job_status(user_id: int, job_id: UUID) -> JobStatusEnum:
    get_and_guard_job(user_id, job_id)
    latest_transition = JobTransitionRepository.get_latest_job_transition(job_id)
    # todo better handling with asserts
    assert latest_transition is not None
    return latest_transition.status
