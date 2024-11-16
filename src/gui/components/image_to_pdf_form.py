import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.image_to_scanned_document.image_to_document_scanner import ImageToPdfScanner

class ImageToPdfForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Configure background and padding
        self.configure(style='Custom.TFrame', padding=20)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # For pushing the last button down
        self.rowconfigure(5, weight=1)

        # Title label
        self.title_label = ttk.Label(self, text="Konverzija slike u skenirani pdf dokument", font=("Helvetica", 14, "bold"),
                                     style="Custom.TLabel")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        # Image selection label
        self.image_label = ttk.Label(self, text="Odaberite sliku za konverziju:", style="Custom.TLabel")
        self.image_label.grid(row=1, column=0, columnspan=2, pady=(5, 5))

        # Image path entry
        self.image_path_entry = ttk.Entry(self, style="Custom.TEntry")
        self.image_path_entry.grid(row=2, column=0, sticky="ew", padx=(0, 5))
        self.image_path_entry.insert(0, "Putanja do slike")

        # Browse button for image
        self.browse_image_button = ttk.Button(self, text="Odaberi sliku", command=self.browse_image, style="Custom.TButton")
        self.browse_image_button.grid(row=2, column=1, sticky="ew")

        # Output folder label
        self.output_label = ttk.Label(self, text="Odaberite izlaznu putanju za PDF:", style="Custom.TLabel")
        self.output_label.grid(row=3, column=0, columnspan=2, pady=(5, 5))

        # Output path entry
        self.output_path_entry = ttk.Entry(self, style="Custom.TEntry")
        self.output_path_entry.grid(row=4, column=0, sticky="ew", padx=(0, 5))
        self.output_path_entry.insert(0, "Putanja za PDF")

        # Browse button for output folder
        self.browse_output_button = ttk.Button(self, text="Odaberi direktorij", command=self.browse_output_folder, style="Custom.TButton")
        self.browse_output_button.grid(row=4, column=1, sticky="ew")

        # Convert button
        self.convert_button = ttk.Button(self, text="Konvertiraj u PDF", command=self.convert_image_to_pdf, style="Custom.TButton")
        self.convert_button.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(10, 5))  # Put button in the last row

        # Set styles
        self.set_styles()

    def set_styles(self):
        """Set custom styles for the form."""
        style = ttk.Style()

        # Frame style with a soft ivory background
        style.configure('Custom.TFrame', background='#fefae0')  # Ivory

        # Label style
        style.configure('Custom.TLabel', background='#fefae0', font=('Helvetica', 12), foreground='#34495e')  # Slate Gray

        # Button style
        style.configure('Custom.TButton',
                        font=('Helvetica', 12),
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
                        font=('Helvetica', 12))

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

        scanner = ImageToPdfScanner(input_image_path, output_pdf_path)

        try:
            scanner.process_and_save()
            messagebox.showinfo("Uspjeh", f"PDF je uspješno spremljen na {output_pdf_path}")
        except Exception as e:
            messagebox.showerror("Greška", f"Došlo je do greške: {str(e)}")

