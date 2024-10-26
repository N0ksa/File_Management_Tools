import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.pdf_moving import process_and_move_pdf

class PdfMoverForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pdf_files = []  # Lista za pohranu PDF datoteka u odabranom direktoriju
        self.destination_folder = None  # Pohrana odredišne mape

        # Dodavanje oznake za sekciju
        self.title_label = ttk.Label(self, text="Premještanje PDF datoteka", font=("Helvetica", 14, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        # Oznaka za odabir direktorija
        self.label = ttk.Label(self, text="Odaberite direktorij s PDF datotekama:")
        self.label.grid(row=1, column=0, columnspan=2, pady=(5, 5))

        # Polje za unos putanje do direktorija
        self.folder_path_entry = ttk.Entry(self)
        self.folder_path_entry.grid(row=2, column=0, sticky="ew", padx=(0, 5))
        self.folder_path_entry.insert(0, "Putanja do direktorija")

        # Gumb za odabir direktorija
        self.browse_button = ttk.Button(self, text="Odaberi direktorij", command=self.browse_folder)
        self.browse_button.grid(row=2, column=1, sticky="ew")

        # Okvir za listbox s PDF datotekama
        self.listbox_frame = ttk.Frame(self)
        self.listbox_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(5, 10))

        # Listbox za prikaz PDF datoteka iz direktorija
        self.file_listbox = tk.Listbox(self.listbox_frame, selectmode=tk.MULTIPLE, height=10)
        self.file_listbox.pack(fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)


        # Gumb za odabir odredišne mape
        self.destination_button = ttk.Button(self, text="Odaberi odredišnu mapu", command=self.select_destination_folder)
        self.destination_button.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)

        # Gumb za premještanje PDF-ova
        self.move_button = ttk.Button(self, text="Premjesti PDF-ove", command=self.move_selected_pdfs)
        self.move_button.grid(row=5, column=0, columnspan=2, sticky="ew", pady=5)

    def browse_folder(self):
        folder_path = filedialog.askdirectory(title="Odaberite direktorij s PDF datotekama")
        if folder_path:
            self.folder_path_entry.delete(0, tk.END)
            self.folder_path_entry.insert(0, folder_path)
            self.load_pdf_files(folder_path)

    def load_pdf_files(self, folder_path):
        """Učitava sve PDF datoteke iz odabranog direktorija u listbox."""
        self.file_listbox.delete(0, tk.END)  # Očistiti trenutnu listu
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
        self.pdf_files = [os.path.join(folder_path, f) for f in pdf_files]  # Puni listu s punim putanjama

        for pdf_file in pdf_files:
            self.file_listbox.insert(tk.END, pdf_file)

    def select_destination_folder(self):
        folder_path = filedialog.askdirectory(title="Odaberite odredišnu mapu")
        if folder_path:
            self.destination_folder = folder_path
            messagebox.showinfo("Odabrana mapa", f"Odabrana odredišna mapa: {self.destination_folder}")

    def move_selected_pdfs(self):
        """Premješta odabrane PDF datoteke u odabranu odredišnu mapu."""
        if not self.pdf_files:
            messagebox.showwarning("Upozorenje", "Niste učitali PDF datoteke.")
            return

        if not self.destination_folder:
            messagebox.showwarning("Upozorenje", "Niste odabrali odredišnu mapu.")
            return

        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Upozorenje", "Molimo odaberite PDF datoteke za premještanje.")
            return

        # Lista odabranih PDF-ova za premještanje
        pdf_files_to_move = [self.pdf_files[index] for index in selected_indices]

        # Premještanje odabranih PDF-ova
        for pdf_path in pdf_files_to_move:
            try:
                process_and_move_pdf(pdf_path, self.destination_folder)
                print(f"Premješteno: {pdf_path}")
            except Exception as e:
                messagebox.showerror("Greška", f"Greška prilikom premještanja {os.path.basename(pdf_path)}: {e}")

        messagebox.showinfo("Uspjeh", "Svi odabrani PDF-ovi su uspješno premješteni.")
        self.load_pdf_files(self.folder_path_entry.get())
