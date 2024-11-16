import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.pdf_moving import process_and_move_pdf


class PdfMoverForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Configure background and padding
        self.configure(style='Custom.TFrame', padding=20)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)  # Adjust row 4 to be resizable

        # Title label
        self.title_label = ttk.Label(self, text="Premještanje PDF datotekama", font=("Arial", 16, "bold"),
                                     style="Custom.TLabel")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 15))

        # Directory selection label
        self.label = ttk.Label(self, text="Odaberite direktorij s PDF datotekama:", style="Custom.TLabel")
        self.label.grid(row=1, column=0, columnspan=2, pady=(5, 10))

        # Entry for folder path
        self.folder_path_entry = ttk.Entry(self, style="Custom.TEntry")
        self.folder_path_entry.grid(row=2, column=0, sticky="ew", padx=(0, 10))
        self.folder_path_entry.insert(0, "Putanja do direktorija")

        # Browse button for directory
        self.browse_button = ttk.Button(self, text="Odaberi direktorij", command=self.browse_folder,
                                        style="Custom.TButton")
        self.browse_button.grid(row=2, column=1, sticky="ew")

        # Entry for destination folder path
        self.destination_path_entry = ttk.Entry(self, style="Custom.TEntry")
        self.destination_path_entry.grid(row=3, column=0, sticky="ew", padx=(0, 10))
        self.destination_path_entry.insert(0, "Putanja do odredišne mape")

        # Browse button for destination folder
        self.destination_button = ttk.Button(self, text="Odaberi odredišnu mapu",
                                             command=self.select_destination_folder,
                                             style="Custom.TButton")
        self.destination_button.grid(row=3, column=1, sticky="ew", pady=(5, 10))

        # Listbox for PDF files with a scroll bar
        self.listbox_frame = ttk.Frame(self)
        self.listbox_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=(10, 15))

        self.file_listbox = tk.Listbox(self.listbox_frame, selectmode=tk.MULTIPLE, height=10, bg="#f9f9f9", bd=0,
                                       highlightthickness=1, font=("Arial", 10))
        self.file_listbox.pack(fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)

        # Add scrollbar to the listbox
        scrollbar = ttk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Move button
        self.move_button = ttk.Button(self, text="Premjesti PDF-ove", command=self.move_selected_pdfs,
                                      style="Custom.TButton")
        self.move_button.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(5, 10))

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
        """Browse and select a folder, then load its PDF files."""
        folder_path = filedialog.askdirectory(title="Odaberite direktorij s PDF datotekama")
        if folder_path:
            self.folder_path_entry.delete(0, tk.END)
            self.folder_path_entry.insert(0, folder_path)
            self.load_pdf_files(folder_path)

    def load_pdf_files(self, folder_path):
        """Load PDF files from the selected folder into the listbox."""
        self.file_listbox.delete(0, tk.END)  # Clear current list
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
        self.pdf_files = [os.path.join(folder_path, f) for f in pdf_files]  # Full paths for processing

        for pdf_file in pdf_files:
            self.file_listbox.insert(tk.END, pdf_file)

    def select_destination_folder(self):
        """Select a destination folder for moving files."""
        folder_path = filedialog.askdirectory(title="Odaberite odredišnu mapu")
        if folder_path:
            self.destination_folder = folder_path
            self.destination_path_entry.delete(0, tk.END)  # Clear any previous path
            self.destination_path_entry.insert(0, folder_path)
            messagebox.showinfo("Odabrana mapa", f"Odabrana odredišna mapa: {self.destination_folder}")

    def move_selected_pdfs(self):
        """Move selected PDF files to the destination folder."""
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

        pdf_files_to_move = [self.pdf_files[index] for index in selected_indices]

        for pdf_path in pdf_files_to_move:
            try:
                process_and_move_pdf(pdf_path, self.destination_folder)
                print(f"Premješteno: {pdf_path}")
            except Exception as e:
                messagebox.showerror("Greška", f"Greška prilikom premještanja {os.path.basename(pdf_path)}: {e}")

        messagebox.showinfo("Uspjeh", "Svi odabrani PDF-ovi su uspješno premješteni.")
        self.load_pdf_files(self.folder_path_entry.get())

