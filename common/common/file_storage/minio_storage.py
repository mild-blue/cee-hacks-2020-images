import io
import logging
from datetime import timedelta
from typing import Tuple, Optional

from minio import Minio
from minio.error import BucketAlreadyOwnedByYou, BucketAlreadyExists, ResponseError

from common.file_storage.file_storage import FileStorage

logger = logging.getLogger(__name__)


class MinIoStorage(FileStorage):

    def __init__(self, minio_url: str,
                 access_key: str,
                 secret_key: str,
                 secure: bool = True) -> None:
        super().__init__()
        self.client = Minio(minio_url,
                            access_key=access_key,
                            secret_key=secret_key,
                            secure=secure)

    def create_folder(self, folder_name: str) -> Tuple[bool, Optional[str]]:
        try:
            self.client.make_bucket(folder_name)
            result = True, None
        except BucketAlreadyOwnedByYou as err:
            logger.debug(f'Trying to create bucket that already exist!', err.message)
            result = False, 'Bucket already exist.'
        except BucketAlreadyExists as err:
            logger.debug(f'Trying to create bucket that already exist!', err.message)
            result = False, 'Bucket already exist.'
        except ResponseError as err:
            logger.exception('Exception during bucket creation!')
            result = False, err.message

        return result

    def delete_folder(self,
                      folder_name: str
                      ) -> Tuple[bool, Optional[str]]:
        try:
            self.client.remove_bucket(bucket_name=folder_name)
            return True, None
        except ResponseError as err:
            logger.exception('Exception during bucket deletion!')
            return False, err.message

    def upload_file(self,
                    folder_name: str,
                    file_path: str,
                    uploaded_file_name: Optional[str] = None
                    ) -> Tuple[bool, Optional[str]]:
        try:
            file_name = uploaded_file_name if uploaded_file_name else 'TODO'
            self.client.fput_object(bucket_name=folder_name,
                                    object_name=file_name,
                                    file_path=file_path)
            return True, None
        except ResponseError as err:
            logger.exception('Exception during file upload!')
            return False, err.message

    def upload_bytes(self,
                     folder_name: str,
                     data: bytes,
                     uploaded_file_name: str
                     ) -> Tuple[bool, Optional[str]]:
        try:
            self.client.put_object(bucket_name=folder_name,
                                   object_name=uploaded_file_name,
                                   data=io.BytesIO(data),
                                   length=len(data))
            return True, None
        except ResponseError as err:
            logger.exception('Exception during file upload!')
            return False, err.message

    def download_bytes(self,
                       folder_name: str,
                       file_name: str
                       ) -> Tuple[bytes, Optional[str]]:
        response = None
        try:
            response = self.client.get_object(bucket_name=folder_name,
                                              object_name=file_name)
            return response.data, None
        except ResponseError as err:
            logger.exception('Exception during file download!')
            return bytes(), err.message
        finally:
            if response:
                response.close()
                response.release_conn()

    def download_file(self,
                      folder_name: str,
                      file_name: str,
                      saving_path: str
                      ) -> Tuple[bool, Optional[str]]:
        try:
            self.client.fget_object(bucket_name=folder_name,
                                    object_name=file_name,
                                    file_path=saving_path)
            return True, None
        except ResponseError as err:
            logger.exception('Exception during the file download.')
            return False, err.message

    def delete_file(self,
                    folder_name: str,
                    file_name: str
                    ) -> Tuple[bool, Optional[str]]:
        try:
            self.client.remove_object(bucket_name=folder_name,
                                      object_name=file_name)
            return True, None
        except ResponseError as err:
            logger.exception('Exception during the file deletion.')
            return False, err.message

    def create_file_url(self,
                        folder_name: str,
                        file_name: str,
                        expires: timedelta) -> str:
        return self.client.presigned_get_object(bucket_name=folder_name,
                                                object_name=file_name,
                                                expires=expires)
