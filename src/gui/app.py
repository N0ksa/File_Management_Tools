import tkinter as tk
from tkinter import ttk

from src.gui.components.pdf_mover_form import PdfMoverForm
from src.gui.components.pdf_renamer_form import PdfRenamerForm


def main():
    app = Application()
    app.mainloop()


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Projekt app")  # Naslov aplikacije
        self.geometry("800x600")  # Dimenzije prozora

        # Povećanje razmaka između elemenata
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Dodavanje glavnog okvira s dvije kolone
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # Kreiranje PdfRenamerForm s lijeve strane
        self.pdf_renamer_form = PdfRenamerForm(self.main_frame)
        self.pdf_renamer_form.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)

        # Kreiranje PdfMoverForm s desne strane
        self.pdf_mover_form = PdfMoverForm(self.main_frame)
        self.pdf_mover_form.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=5)


if __name__ == "__main__":
    main()



