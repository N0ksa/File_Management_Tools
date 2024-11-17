import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.image_to_scanned_document.image_to_document_scanner import ImageToPdfScanner
from src.utils.exception_handler import ExceptionHandler


class ImageToPdfForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.exception_handler = ExceptionHandler()


        self.configure(style='Custom.TFrame', padding=20)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(5, weight=1)


        self.title_label = ttk.Label(self, text="Konverzija slike u skenirani pdf dokument", font=("Helvetica", 14, "bold"),
                                     style="Custom.TLabel")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))


        self.image_label = ttk.Label(self, text="Odaberite sliku za konverziju:", style="Custom.TLabel")
        self.image_label.grid(row=1, column=0, columnspan=2, pady=(5, 5))


        self.image_path_entry = ttk.Entry(self, style="Custom.TEntry")
        self.image_path_entry.grid(row=2, column=0, sticky="ew", padx=(0, 5))
        self.image_path_entry.insert(0, "Putanja do slike")


        self.browse_image_button = ttk.Button(self, text="Odaberi sliku", style="Custom.TButton",
                                              command=self.browse_image)
        self.browse_image_button.grid(row=2, column=1, sticky="ew", padx=(5, 0))


        self.output_label = ttk.Label(self, text="Odaberite izlaznu putanju:", style="Custom.TLabel")
        self.output_label.grid(row=3, column=0, columnspan=2, pady=(5, 5))


        self.output_path_entry = ttk.Entry(self, style="Custom.TEntry")
        self.output_path_entry.grid(row=4, column=0, sticky="ew", padx=(0, 5))
        self.output_path_entry.insert(0, "Putanja za pdf")


        self.browse_output_button = ttk.Button(self, text="Odaberi PDF", style="Custom.TButton",
                                               command=self.browse_output)
        self.browse_output_button.grid(row=4, column=1, sticky="ew", padx=(5, 0))


        self.convert_button = ttk.Button(self, text="Konvertiraj", style="Custom.TButton", command=self.convert_image_to_pdf)
        self.convert_button.grid(row=5, column=0, columnspan=2, pady=(20, 10))

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_path_entry.delete(0, tk.END)
            self.image_path_entry.insert(0, file_path)

    def browse_output(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, file_path)

    def convert_image_to_pdf(self):
        input_image_path = self.image_path_entry.get()
        output_pdf_path = self.output_path_entry.get()

        if not input_image_path or not os.path.isfile(input_image_path):
            messagebox.showwarning("Pogreška", "Molim odaberite valjanu sliku!")
            return

        if not output_pdf_path:
            messagebox.showwarning("Pogreška", "Molim odaberite odredište za PDF datoteku!")
            return

        scanner = ImageToPdfScanner(input_image_path, output_pdf_path)

        try:
            scanner.process_and_save()
            messagebox.showinfo("Uspjeh", f"PDF uspješno spremljen u {output_pdf_path}")

        except Exception as e:
            self.exception_handler.log_exception(e)
            self.exception_handler.show_user_message("Dogodila se pogreška. Za više detalja pogledajte log datoteku.")
