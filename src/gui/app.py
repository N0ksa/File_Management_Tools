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
        self.geometry("800x600")  # Dimenzije prozora (povećano da bi obje komponente stale)

        # Dodavanje okvira s naslovom
        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(pady=10)

        self.title_label = ttk.Label(self.title_frame, text="Projekt app", font=("Helvetica", 16))
        self.title_label.pack()

        # Povećanje razmaka između elemenata
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Dodavanje glavnog okvira
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Kreiranje PdfRenamerForm i PdfMoverForm unutar glavnog okvira
        self.pdf_renamer_form = PdfRenamerForm(self.main_frame)
        self.pdf_renamer_form.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.pdf_mover_form = PdfMoverForm(self.main_frame)
        self.pdf_mover_form.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)




if __name__ == "__main__":
    main()



