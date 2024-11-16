from tkinter import ttk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import concurrent.futures
from src.pdf_renaming.pdf_renamer import PdfRenamer  # Import the PdfRenamer class


class PdfRenamerForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Configure background and padding
        self.configure(style='Custom.TFrame', padding=20)  # Add padding to the form

        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        # Title label with improved styling
        self.title_label = ttk.Label(self, text="Preimenovanje PDF datoteka", font=("Arial", 16, "bold"),
                                     style="Custom.TLabel")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 15))

        # Directory selection label
        self.label = ttk.Label(self, text="Odaberite direktorij s PDF datotekama:", style="Custom.TLabel")
        self.label.grid(row=1, column=0, columnspan=2, pady=(5, 10))

        # Entry for folder path with better style and thickness
        self.folder_path_entry = ttk.Entry(self, style="Custom.TEntry")
        self.folder_path_entry.grid(row=2, column=0, sticky="ew", padx=(0, 10))
        self.folder_path_entry.insert(0, "Putanja do direktorija")

        # Browse button
        self.browse_button = ttk.Button(self, text="Odaberi direktorij", command=self.browse_folder,
                                        style="Custom.TButton")
        self.browse_button.grid(row=2, column=1, sticky="ew")

        # Listbox for PDF files with a scroll bar
        self.listbox_frame = ttk.Frame(self)
        self.listbox_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(10, 15))

        self.pdf_listbox = tk.Listbox(self.listbox_frame, selectmode=tk.MULTIPLE, height=10, bg="#f9f9f9", bd=0,
                                      highlightthickness=1, font=("Arial", 10))
        self.pdf_listbox.pack(fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)

        # Rename button
        self.rename_button = ttk.Button(self, text="Obradi PDF", command=self.process_pdfs, style="Custom.TButton")
        self.rename_button.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(5, 10))

        # Add scrollbar to the listbox
        scrollbar = ttk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL, command=self.pdf_listbox.yview)
        self.pdf_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Set styles
        self.set_styles()

    def set_styles(self):
        """Set custom styles for the form."""
        style = ttk.Style()

        # Frame style with a soft ivory background
        style.configure('Custom.TFrame', background='#fefae0')  # Ivory

        # Label style
        style.configure('Custom.TLabel', background='#fefae0', font=('Arial', 14), foreground='#34495e')  # Slate Gray

        # Button style
        style.configure('Custom.TButton',
                        font=('Arial', 12),
                        padding=10,
                        background='#4caf50')  # Green
        style.map('Custom.TButton',
                  background=[('active', '#388e3c'),  # Darker green on hover
                              ('pressed', '#2e7d32')])  # Even darker green on click

        # Entry style with modern design and thickness
        style.configure('Custom.TEntry',
                        fieldbackground='#ffffff',  # White background
                        bordercolor='#34495e',  # Slate Gray border
                        padding=10,
                        font=('Arial', 12))

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path_entry.delete(0, tk.END)
            self.folder_path_entry.insert(0, folder_path)
            self.load_pdf_files(folder_path)

    def load_pdf_files(self, folder_path):
        self.pdf_listbox.delete(0, tk.END)
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

        # Create a PdfRenamer instance and process PDFs
        pdf_renamer = PdfRenamer(folder_path, pdf_files_to_process)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(pdf_renamer.process_pdfs)

        messagebox.showinfo("Uspjeh", "PDF datoteke su uspješno obrađene.")
