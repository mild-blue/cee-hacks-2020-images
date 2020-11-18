import os

import pytesseract
from PIL import Image
from pdf2image import convert_from_path

# path to the folder with medical reports
PATH_TO_DATA_DIR = "/home/ub/Downloads/zpravy"
DPI = 500
TMP_FILE = "tmp"


def main():
    # iterate PDFs one by one
    for filename in os.listdir(PATH_TO_DATA_DIR):
        # convert to jpeg page by page
        pages = convert_from_path(os.path.join(PATH_TO_DATA_DIR, filename), DPI)
        # prepare output file
        outfile = f"{os.path.join(PATH_TO_DATA_DIR, filename)}.txt"
        with open(outfile, "a") as f:
            # read page by page
            for page in pages:
                # save tmp image
                page.save(TMP_FILE, 'JPEG')
                # Recognize the text as string in image using pytesseract
                text = str((pytesseract.image_to_string(Image.open(TMP_FILE))))
                # store text to .txt
                f.write(text)
                # clean up
                os.remove(TMP_FILE)


if __name__ == '__main__':
    main()
