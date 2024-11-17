from tkinter import ttk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import concurrent.futures
from src.pdf_renaming.pdf_renamer import PdfRenamer
import threading


class PdfRenamerForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)


        self.configure(style='Custom.TFrame', padding=20)  # Add padding to the form

        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)


        self.title_label = ttk.Label(self, text="Preimenovanje PDF datoteka", font=("Arial", 16, "bold"),
                                     style="Custom.TLabel")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 15))


        self.label = ttk.Label(self, text="Odaberite direktorij s PDF datotekama:", style="Custom.TLabel")
        self.label.grid(row=1, column=0, columnspan=2, pady=(5, 10))


        self.folder_path_entry = ttk.Entry(self, style="Custom.TEntry")
        self.folder_path_entry.grid(row=2, column=0, sticky="ew", padx=(0, 10))
        self.folder_path_entry.insert(0, "Putanja do direktorija")


        self.browse_button = ttk.Button(self, text="Odaberi direktorij", command=self.browse_folder,
                                        style="Custom.TButton")
        self.browse_button.grid(row=2, column=1, sticky="ew")


        self.listbox_frame = ttk.Frame(self)
        self.listbox_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(10, 15))

        self.pdf_listbox = tk.Listbox(self.listbox_frame, selectmode=tk.MULTIPLE, height=10, bg="#f9f9f9", bd=0,
                                      highlightthickness=1, font=("Arial", 10))
        self.pdf_listbox.pack(fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)


        self.rename_button = ttk.Button(self, text="Obradi PDF", command=self.start_rename_pdfs_thread, style="Custom.TButton")
        self.rename_button.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(5, 10))


        scrollbar = ttk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL, command=self.pdf_listbox.yview)
        self.pdf_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


        self.set_styles()


        self.progressbar = ttk.Progressbar(self, orient="horizontal", mode="indeterminate", length=300)
        self.progressbar.grid(row=5, column=0, columnspan=2, pady=(10, 15))
        self.progressbar.grid_remove()  # Hide the progress bar initially

    def set_styles(self):
        """Set custom styles for the form."""
        style = ttk.Style()


        style.configure('Custom.TFrame', background='#fefae0')  # Ivory


        style.configure('Custom.TLabel', background='#fefae0', font=('Arial', 14), foreground='#34495e')  # Slate Gray


        style.configure('Custom.TButton',
                        font=('Arial', 12),
                        padding=10,
                        background='#4caf50')  # Green
        style.map('Custom.TButton',
                  background=[('active', '#388e3c'),  # Darker green on hover
                              ('pressed', '#2e7d32')])  # Even darker green on click


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

    def start_rename_pdfs_thread(self):
        folder_path = self.folder_path_entry.get()

        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showwarning("Upozorenje", "Molimo unesite valjanu putanju do direktorija.")
            return

        selected_files = self.pdf_listbox.curselection()

        if not selected_files:
            messagebox.showwarning("Upozorenje", "Molimo odaberite PDF datoteke za obradu.")
            return


        self.rename_button.config(state=tk.DISABLED)


        self.progressbar.grid()
        self.progressbar.start()


        threading.Thread(target=self.process_pdfs).start()

    def process_pdfs(self):
        folder_path = self.folder_path_entry.get()
        selected_files = self.pdf_listbox.curselection()

        pdf_files_to_process = [os.path.join(folder_path, self.pdf_listbox.get(index)) for index in selected_files]

        pdf_renamer = PdfRenamer(folder_path, pdf_files_to_process)

        total_success, total_error = pdf_renamer.process_pdfs()


        self.after(0, lambda: self.progressbar.grid_remove())
        self.after(0, lambda: self.rename_button.config(state=tk.NORMAL))


        if total_success > 0 and total_error == 0:
            self.after(0, lambda: messagebox.showinfo("Uspjeh", f"Obrada je završena!\n\n"
                                                                f"Uspješno preimenovano: {total_success} PDF datoteka"))
        elif total_success > 0:
            self.after(0, lambda: messagebox.showinfo("Uspjeh", f"Obrada je završena!\n\n"
                                                                f"Uspješno preimenovano: {total_success} PDF datoteka\n"
                                                                f"Neuspješno preimenovano: {total_error} PDF datoteka. Pogledajte log datoteku za više detalja"))
        else:
            self.after(0, lambda: messagebox.showerror("Neuspjeh",
                                                       f"Niti jedna PDF datoteka nije uspješno preimenovana.\n\n"
                                                       "Molimo provjerite log datoteku za više detalja o greškama."))
