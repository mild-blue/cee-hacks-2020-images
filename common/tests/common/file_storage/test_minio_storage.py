from uuid import uuid4

from tests.test_base import BaseTest

from common.file_storage.minio_storage import MinIoStorage


class TestMinioStorage(BaseTest):

    @staticmethod
    def _get_storage() -> MinIoStorage:
        # this is actually working public instance
        return MinIoStorage('play.min.io',
                            access_key='Q3AM3UQ867SPQQA43P2F',
                            secret_key='zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG',
                            secure=True)

    def test_init_client(self):
        self.assertIsNotNone(self._get_storage())

    def test_create_bytes_and_download(self):
        storage = self._get_storage()

        original_message = 'hello world'

        data = original_message.encode()
        folder = str(uuid4())
        file_name = f'{uuid4()}.bin'

        created, message = storage.create_folder(folder)
        self.assertTrue(created)
        self.assertIsNone(message)

        created, message = storage.upload_bytes(folder_name=folder,
                                                data=data,
                                                uploaded_file_name=file_name)
        self.assertTrue(created)
        self.assertIsNone(message)

        bytes_data, message = storage.download_bytes(folder_name=folder,
                                                     file_name=file_name)
        self.assertIsNotNone(bytes_data)
        self.assertIsNone(message)

        received_message = bytes_data.decode()

        self.assertEqual(original_message, received_message)
