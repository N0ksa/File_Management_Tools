import os
import re
import pytesseract

from src.preprocessing import extract_text_from_pdf
from src.utils import move_pdf_to_folder
from src.utils import find_name_surname_date

# Putanja do instalacije Tesseract OCR-a
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Funkcija za pronalaženje imena poslodavca
def find_employer(text):
    employer_pattern = re.compile(r'Poslodavac:\s*([A-ZČĆŽŠĐa-zčćžšđ]+(?:\s+[A-ZČĆŽŠĐa-zčćžšđ]+){0,1})', re.IGNORECASE)
    employer_match = employer_pattern.search(text)
    return employer_match.group(1) if employer_match else None


# Funkcija za obradu pojedinog PDF-a s odabranom destinacijom
def process_and_move_pdf(pdf_path, destination_folder):
    try:
        text = extract_text_from_pdf(pdf_path)

        # Predefinirane podmape unutar destinacijske mape
        vozaci_subfolder = os.path.join(destination_folder, "3. Vozači")
        prekvalifikacija_subfolder = os.path.join(destination_folder, "2. Prekvalifikacija; Škole; Učilišta; Obrt; Komore; Ostalo")
        sportasi_subfolder = os.path.join(destination_folder, "4. Sportaši")
        pomorci_subfolder = os.path.join(destination_folder, "5. Pomorci")

        if re.search(r'UVJERENJE\s*o\s*zdravstvenoj\s*sposobnosti\s*za\s*upravljanje\s*vozilima', text, re.IGNORECASE):
            os.makedirs(vozaci_subfolder, exist_ok=True)
            move_pdf_to_folder(pdf_path, vozaci_subfolder)

        elif re.search(r'UVJERENJE\s*o\s*zdravstvenoj\s*sposobnosti\s*radnika', text, re.IGNORECASE):
            name_surname_date = find_name_surname_date(text)
            employer = find_employer(text)
            if name_surname_date and name_surname_date[0] and employer:
                name_surname = name_surname_date[0]
                employer_folder = os.path.join(destination_folder, employer)
                final_destination = os.path.join(employer_folder, name_surname)
                os.makedirs(final_destination, exist_ok=True)
                move_pdf_to_folder(pdf_path, final_destination)
            else:
                print("Could not find the required information in the PDF.")

        elif re.search(r'UVJERENJE\s*O\s*ZDRAVSTVENOJ\s*SPOSOBNOSTI\s*\n\s*ZA\s*OBRAZOVANJE', text, re.IGNORECASE):
            os.makedirs(prekvalifikacija_subfolder, exist_ok=True)
            move_pdf_to_folder(pdf_path, prekvalifikacija_subfolder)

        elif re.search(r'LIJEČNIČKA\s*SVJEDODŽBA', text, re.IGNORECASE):
            os.makedirs(prekvalifikacija_subfolder, exist_ok=True)
            move_pdf_to_folder(pdf_path, prekvalifikacija_subfolder)

        elif re.search(r'UVJERENJE\s*O\s*ZDRAVSTVENOJ\s*SPOSOBNOSTI\s*\n\s*SPORTAŠA', text, re.IGNORECASE) or re.search(
                r'UVJERENJE\s*O\s*ZDRAVSTVENOJ\s*SPOSOBNOSTI\s*\n\s*SPORTASA', text, re.IGNORECASE):
            os.makedirs(sportasi_subfolder, exist_ok=True)
            move_pdf_to_folder(pdf_path, sportasi_subfolder)

        elif re.search(r'o\s*zdravstvenoj\s*sposobnosti\s*člana\s*posade\s*pomorskog\s*broda', text, re.IGNORECASE):
            os.makedirs(pomorci_subfolder, exist_ok=True)
            move_pdf_to_folder(pdf_path, pomorci_subfolder)

        else:
            print("Document type not recognized.")

    except Exception as e:
        print(f"Error in process_and_move_pdf: {e}")
