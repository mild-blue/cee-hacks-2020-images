import json
import os
import tempfile
from typing import Tuple
from uuid import UUID

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from backend.service.file_storage import get_file_storage
from common.enums.job_status_enum import JobStatusEnum
from common.service.job_service import JobService
from common.constants import INPUT_FILE_NAME, METADATA_FILE_NAME


def create_new_job(user_id: int, request_stream: FileStorage, metadata: dict) -> Tuple[UUID, JobStatusEnum]:
    fs = get_file_storage()
    # TODO obtain correct file type ending

    # create job in the database
    job = JobService.create_job(user_id)
    # TODO better handling
    assert job is not None

    # create the file folder
    created, error = fs.create_folder(str(job.id))
    if not created:
        raise Exception(error)

    # upload the metadata
    json_meta = json.dumps(metadata)
    uploaded, error = fs.upload_bytes(str(job.id), json_meta.encode(), METADATA_FILE_NAME)
    if not uploaded:
        raise Exception(error)

    # save the file locally
    # TODO ensure that temp_file_name is actually unique
    temp_file_name = secure_filename(request_stream.filename)
    temp_file_path = os.path.join(tempfile.gettempdir(), temp_file_name)
    request_stream.save(temp_file_path)

    # upload file to storage
    # TODO correct naming and types
    uploaded, error = fs.upload_file(str(job.id), temp_file_path, uploaded_file_name=INPUT_FILE_NAME)
    if not uploaded:
        raise Exception(error)

    # delete temp file from the local storage
    os.remove(temp_file_path)

    # queue the job
    transition = JobService.add_job_status(job.id, JobStatusEnum.QUEUED)
    assert transition is not None
    return job.id, transition.status
