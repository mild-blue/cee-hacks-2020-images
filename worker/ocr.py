import logging
import time

logger = logging.getLogger('worker')


def run_ocr(file_path: str, metadata: dict) -> str:
    """
    Run OCR algorithm, `file_path` is path to the image with the input
    and `metadata` is the dictionary sent by client.
    The method returns recognized text.
    """
    time.sleep(10)
    return 'no data'


if __name__ == '__main__':
    run_ocr('some_file_locally', {})
