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

def convert_images_to_txt(image_paths: list, txt_path: str, languages='hrv+fra+deu') -> None:
    all_extracted_text = ""

    for img_path in image_paths:
        try:
            img = Image.open(img_path)
            extracted_text = extract_text_from_image(img, languages)

            all_extracted_text += extracted_text + "\n"

        except Exception as e:
            print(f"Error processing {img_path}: {e}")

    # Save the extracted text to a .txt file
    with open(txt_path, 'w', encoding='utf-8') as text_file:
        text_file.write(all_extracted_text)
    print(f"Extracted text saved to: {txt_path}")



