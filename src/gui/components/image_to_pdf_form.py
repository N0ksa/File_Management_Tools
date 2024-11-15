import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.image_to_scanned_document.image_to_document_scanner import ImageToPdfScanner

class ImageToPdfForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(5, weight=1)

        # Title label for the section
        self.title_label = ttk.Label(self, text="Konverzija slike u skenirani pdf dokument", font=("Helvetica", 14, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        # Label for selecting image
        self.image_label = ttk.Label(self, text="Odaberite sliku za konverziju:")
        self.image_label.grid(row=1, column=0, columnspan=2, pady=(5, 5))

        # Entry field for image path
        self.image_path_entry = ttk.Entry(self)
        self.image_path_entry.grid(row=2, column=0, sticky="ew", padx=(0, 5))
        self.image_path_entry.insert(0, "Putanja do slike")

        # Button to browse image
        self.browse_image_button = ttk.Button(self, text="Odaberi sliku", command=self.browse_image)
        self.browse_image_button.grid(row=2, column=1, sticky="ew")

        # Label for selecting output path
        self.output_label = ttk.Label(self, text="Odaberite izlaznu putanju za PDF:")
        self.output_label.grid(row=3, column=0, columnspan=2, pady=(5, 5))

        # Entry field for output path
        self.output_path_entry = ttk.Entry(self)
        self.output_path_entry.grid(row=4, column=0, sticky="ew", padx=(0, 5))
        self.output_path_entry.insert(0, "Putanja za PDF")

        # Button to browse output folder
        self.browse_output_button = ttk.Button(self, text="Odaberi direktorij", command=self.browse_output_folder)
        self.browse_output_button.grid(row=4, column=1, sticky="ew")

        # Add a blank row (row 5) with weight for stretching the form vertically
        self.rowconfigure(5, weight=1)  # Ensure that row 5 can expand

        # Button to start the PDF conversion process
        self.convert_button = ttk.Button(self, text="Konvertiraj u PDF", command=self.convert_image_to_pdf)
        self.convert_button.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(10, 5))  # Put button in the last row

    def browse_image(self):
        file_path = filedialog.askopenfilename(title="Odaberite sliku",
                                               filetypes=(("Image Files", "*.jpg;*.jpeg;*.png"), ("All Files", "*.*")))
        if file_path:
            self.image_path_entry.delete(0, tk.END)
            self.image_path_entry.insert(0, file_path)

    def browse_output_folder(self):
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if output_path:
            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, output_path)

    def convert_image_to_pdf(self):
        input_image_path = self.image_path_entry.get()
        output_pdf_path = self.output_path_entry.get()

        if not input_image_path or not os.path.isfile(input_image_path):
            messagebox.showwarning("Greška", "Molimo odaberite valjanu sliku!")
            return

        if not output_pdf_path:
            messagebox.showwarning("Greška", "Molimo odaberite izlaznu putanju za PDF!")
            return

        # Create an instance of ImageToPdfScanner
        scanner = ImageToPdfScanner(input_image_path, output_pdf_path)

        try:
            scanner.process_and_save()
            messagebox.showinfo("Uspjeh", f"PDF je uspješno spremljen na {output_pdf_path}")
        except Exception as e:
            messagebox.showerror("Greška", f"Došlo je do greške: {str(e)}")
