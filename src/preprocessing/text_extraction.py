import concurrent
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

from src.config import TESSERACT_CMD
from src.preprocessing.image_processing import preprocess_image

# Postavite putanju do Tesseract-a
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def extract_text_from_image(image, languages='hrv+fra+deu'):
    image = preprocess_image(image)
    return pytesseract.image_to_string(image, lang=languages)

def extract_text_from_pdf(pdf_path, max_pages=2, languages='hrv+fra+deu'):
    pages = convert_from_path(pdf_path, first_page=1, last_page=max_pages)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        texts = executor.map(lambda page: extract_text_from_image(page, languages), pages)
    return ''.join(texts)


def convert_image_to_txt(image_path: str, languages='hrv+fra+deu') -> str:
    """Extract text from a single image and return the extracted text."""
    extracted_text = ""

    try:
        # Open the image
        img = Image.open(image_path)

        # Extract text from the image using pytesseract
        extracted_text = extract_text_from_image(img, languages=languages)

    except Exception as e:
        print(f"Error processing {image_path}: {e}")

    return extracted_text



