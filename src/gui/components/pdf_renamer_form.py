from tkinter import ttk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import concurrent.futures
from src.pdf_renaming.pdf_renamer import process_and_rename_pdf

class PdfRenamerForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Dodavanje oznake za sekciju
        self.title_label = ttk.Label(self, text="Preimenovanje PDF datoteka", font=("Helvetica", 14, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        # Oznaka za odabir direktorija
        self.label = ttk.Label(self, text="Odaberite direktorij s PDF datotekama:")
        self.label.grid(row=1, column=0, columnspan=2, pady=(5, 5))

        # Polje za odabir direktorija
        self.folder_path_entry = ttk.Entry(self)
        self.folder_path_entry.grid(row=2, column=0, sticky="ew", padx=(0, 5))
        self.folder_path_entry.insert(0, "Putanja do direktorija")

        # Gumb za odabir direktorija
        self.browse_button = ttk.Button(self, text="Odaberi direktorij", command=self.browse_folder)
        self.browse_button.grid(row=2, column=1, sticky="ew")

        # Okvir za listbox s PDF datotekama
        self.listbox_frame = ttk.Frame(self)
        self.listbox_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(5, 10))

        # Lista za prikaz PDF datoteka
        self.pdf_listbox = tk.Listbox(self.listbox_frame, selectmode=tk.MULTIPLE, height=10)
        self.pdf_listbox.pack(fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)


        # Gumb za preimenovanje
        self.rename_button = ttk.Button(self, text="Obradi PDF", command=self.process_pdfs)
        self.rename_button.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(5, 10))

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path_entry.delete(0, tk.END)
            self.folder_path_entry.insert(0, folder_path)
            self.load_pdf_files(folder_path)

    def load_pdf_files(self, folder_path):
        self.pdf_listbox.delete(0, tk.END)  # Očistiti trenutnu listu
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
        for pdf_file in pdf_files:
            self.pdf_listbox.insert(tk.END, pdf_file)

    def process_pdfs(self):
        folder_path = self.folder_path_entry.get()

        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showwarning("Upozorenje", "Molimo unesite valjanu putanju do direktorija.")
            return

        selected_files = self.pdf_listbox.curselection()

        if not selected_files:
            messagebox.showwarning("Upozorenje", "Molimo odaberite PDF datoteke za obradu.")
            return

        pdf_files_to_process = [os.path.join(folder_path, self.pdf_listbox.get(index)) for index in selected_files]

        # Obrada PDF datoteka
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(process_and_rename_pdf, pdf_files_to_process)

        messagebox.showinfo("Uspjeh", "PDF datoteke su uspješno obrađene.")
