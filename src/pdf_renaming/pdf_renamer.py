import os
from src.preprocessing import extract_text_from_pdf
from src.utils import find_name_surname_date


class PdfRenamer:
    def __init__(self, folder_path, pdf_files):
        self.folder_path = folder_path
        self.pdf_files = pdf_files

    def rename_pdf(self, pdf_path, name_surname, date):
        try:
            new_filename = f"{name_surname} - Karton {date}.pdf"
            new_filepath = os.path.join(os.path.dirname(pdf_path), new_filename)
            os.rename(pdf_path, new_filepath)
            print(f"Renamed file to: {new_filepath}")
        except Exception as e:
            print(f"Error in rename_pdf: {e}")

    def process_pdf(self, pdf_path):
        try:
            text = extract_text_from_pdf(pdf_path)
            name_surname_date = find_name_surname_date(text)

            if name_surname_date and name_surname_date[0] and name_surname_date[1]:
                name_surname, date = name_surname_date
                self.rename_pdf(pdf_path, name_surname, date)
            else:
                print("Could not find the required information in the PDF.")
        except Exception as e:
            print(f"Error in process_pdf: {e}")

    def process_pdfs(self):
        for pdf_file in self.pdf_files:
            self.process_pdf(pdf_file)
