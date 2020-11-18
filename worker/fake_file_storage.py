import logging
from typing import Tuple, Optional

from common.file_storage.file_storage import FileStorage

logger = logging.getLogger('worker')


class FakeFileStorage(FileStorage):

    def create_folder(self, folder_name: str) -> Tuple[bool, Optional[str]]:
        return True, folder_name

    def delete_folder(self, folder_name: str) -> Tuple[bool, Optional[str]]:
        return True, folder_name

    def upload_file(
            self,
            folder_name: str,
            file_path: str,
            uploaded_file_name: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]:
        return True, uploaded_file_name

    def upload_bytes(
            self,
            folder_name: str,
            data: bytes,
            uploaded_file_name: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]:
        return True, uploaded_file_name

    def download_bytes(
            self,
            folder_name: str,
            file_name: str
    ) -> Tuple[bytes, Optional[str]]:
        return 'Hello.'.encode('utf_8'), file_name

    def delete_file(
            self,
            folder_name: str,
            file_name: str
    ) -> Tuple[bool, Optional[str]]:
        return True, file_name
