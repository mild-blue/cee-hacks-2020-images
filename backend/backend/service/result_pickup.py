from common.constants import OUTPUT_FILE_NAME
from datetime import timedelta
from typing import Union
from uuid import UUID

from backend.service import get_and_guard_job
from backend.service.file_storage import get_file_storage
from common.db.repository.job_transition_repository import JobTransitionRepository
from common.enums.job_status_enum import JobStatusEnum
from common.file_storage.minio_storage import MinIoStorage


def obtain_job_result(user_id: int, job_id: UUID) -> Union[bytes, str]:
    """
    Returns bytes if the file was read, returns string if the file must be read
    from the remote file storage
    """
    get_and_guard_job(user_id, job_id)
    latest_transition = JobTransitionRepository.get_latest_job_transition(job_id)
    if not latest_transition or latest_transition.status != JobStatusEnum.FINISHED:
        # TODO custom exceptions
        raise Exception(f'Job {job_id} is not in FINISHED state but rather in {latest_transition}.')

    fs = get_file_storage()
    # TODO enable redirects as soon as we know how to prevent redirecting with
    # TODO authorization header and how to generate valid urls
    if isinstance(fs, MinIoStorage) and False:
        # noinspection PyTypeChecker
        # we know that this is indeed MinIoStorage because of the check
        return _obtain_url_for_file(fs, job_id)
    else:
        # TODO implement other storages
        data, error = fs.download_bytes(str(job_id), OUTPUT_FILE_NAME)
        if not data:
            raise Exception(error)
        return data


def _obtain_url_for_file(fs: MinIoStorage, job_id: UUID) -> str:
    # TODO correct naming, unify that
    # TODO have the delta somewhere in the config
    return fs.create_file_url(str(job_id), OUTPUT_FILE_NAME, expires=timedelta(minutes=1))
