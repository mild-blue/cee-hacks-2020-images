from typing import Tuple, Optional


class FileStorage:
    def create_folder(self,
                      folder_name: str
                      ) -> Tuple[bool, Optional[str]]:
        pass

    def delete_folder(self,
                      folder_name: str
                      ) -> Tuple[bool, Optional[str]]:
        pass

    def upload_file(self,
                    folder_name: str,
                    file_path: str,
                    uploaded_file_name: Optional[str] = None
                    ) -> Tuple[bool, Optional[str]]:
        pass

    def upload_bytes(self,
                     folder_name: str,
                     data: bytes,
                     uploaded_file_name: str
                     ) -> Tuple[bool, Optional[str]]:
        pass

    def download_bytes(self,
                       folder_name: str,
                       file_name: str
                       ) -> Tuple[bytearray, Optional[str]]:
        pass

    def download_file(self,
                      folder_name: str,
                      file_name: str,
                      saving_path: str
                      ) -> Tuple[bool, Optional[str]]:
        pass

    def delete_file(self,
                    folder_name: str,
                    file_name: str
                    ) -> Tuple[bool, Optional[str]]:
        pass
