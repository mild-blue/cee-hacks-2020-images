from backend.configuration.application_configuration import get_application_configuration
from common.file_storage.file_storage import FileStorage
from common.file_storage.minio_storage import MinIoStorage


def get_file_storage() -> FileStorage:
    """
    Creates instance of FileStorage.
    """
    conf = get_application_configuration()
    return MinIoStorage(conf.minio_url,
                        access_key=conf.minio_access_key,
                        secret_key=conf.minio_secret_key,
                        secure=conf.minio_secure)
