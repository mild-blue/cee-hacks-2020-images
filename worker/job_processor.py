import json
import logging
import os
import pathlib
import tempfile
from typing import Any, Optional, Callable

from common.constants import INPUT_FILE_NAME, METADATA_FILE_NAME, OUTPUT_FILE_NAME
from common.db.database import build_database_configuration_from_env, prepare_db_session, close_db
from common.enums.job_status_enum import JobStatusEnum
from common.file_storage.minio_storage import MinIoStorage
from common.service.job_service import JobService
from dotenv import load_dotenv

from job_dto import JobDto
from ocr import run_ocr

logger = logging.getLogger('worker')

file_storage: MinIoStorage = MinIoStorage(
    minio_url=os.environ.get('MINIO_URL'),
    access_key=os.environ.get('MINIO_ACCESS_KEY'),
    secret_key=os.environ.get('MINIO_SECRET_KEY'),
    secure=os.environ.get('MINIO_SECURE') == 'true'
)


def process_job() -> None:
    logger.info('Getting job for processing.')
    job_dto: Optional[JobDto] = _in_session_scope(lambda: _get_job_to_process())
    if job_dto is None:
        logger.info('No job to process.')
        return

    logger.info(f'Processing of job {job_dto.id}.')
    status = JobStatusEnum.FINISHED

    try:
        _process_ocr(job_dto)
    except Exception as ex:
        logger.error(f'Error while processing job {job_dto.id}.', ex)
        status = JobStatusEnum.FAILURE

    _in_session_scope(lambda: JobService.add_job_status(job_dto.id, status))

    logger.info(f'Processing of job {job_dto.id} done.')


def _process_ocr(job: JobDto) -> None:
    logger.info('Processing OCR.')
    logger.info(f'Loading input file {job.id}/{INPUT_FILE_NAME}.')

    input_file_path = os.path.join(tempfile.gettempdir(), INPUT_FILE_NAME)
    downloaded, error = file_storage.download_file(str(job.id), INPUT_FILE_NAME, input_file_path)
    if not downloaded:
        # todo error handling
        raise Exception(error)
    logger.info(f'Input file {job.id}/{INPUT_FILE_NAME} loaded.')

    metadata_bytes, error = file_storage.download_bytes(str(job.id), METADATA_FILE_NAME)
    if not metadata_bytes:
        # todo error handling
        raise Exception(error)
    metadata = json.loads(metadata_bytes.decode())

    logger.info('Processing.')
    result = run_ocr(input_file_path, metadata)
    logger.info('Processing done.')

    logger.info('Storing results.')
    uploaded, error = file_storage.upload_bytes(str(job.id), result.encode(), OUTPUT_FILE_NAME)
    if not uploaded:
        # todo error handling
        raise Exception(error)
    logger.info('Storing done.')
    logger.info('Cleaning up.')
    os.remove(input_file_path)
    logger.info('Processing OCR done.')


def _init_db() -> None:
    load_dotenv(dotenv_path=os.path.join(pathlib.Path().absolute(), '../.env.test'))
    prepare_db_session(build_database_configuration_from_env(), None)


def _close_db() -> None:
    close_db()


def _in_session_scope(fnc: Callable[[None], Any]) -> Any:
    _init_db()
    result: Any = fnc()
    _close_db()
    return result


def _get_job_to_process() -> Optional[JobDto]:
    job = JobService.get_queued_job_to_process_and_set_it_to_in_progress()
    return None if job is None else JobDto(job.id)
