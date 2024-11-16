import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.preprocessing.text_extraction import  extract_text_from_pdf, convert_image_to_txt


class TextConverterForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Configure background and padding
        self.configure(style='Custom.TFrame', padding=20)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        # Title label
        self.title_label = ttk.Label(self, text="Ekstrakcija teksta iz slike ili PDF-a", font=("Arial", 16, "bold"),
                                     style="Custom.TLabel")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 15))

        # Directory selection label
        self.label = ttk.Label(self, text="Odaberite sliku ili PDF za ekstrakciju teksta:", style="Custom.TLabel")
        self.label.grid(row=1, column=0, columnspan=2, pady=(5, 10))

        # Entry for folder path
        self.folder_path_entry = ttk.Entry(self, style="Custom.TEntry")
        self.folder_path_entry.grid(row=2, column=0, sticky="ew", padx=(0, 10))
        self.folder_path_entry.insert(0, "Putanja do direktorija")

        # Browse button
        self.browse_button = ttk.Button(self, text="Odaberi sliku ili PDF", command=self.browse_file,
                                        style="Custom.TButton")
        self.browse_button.grid(row=2, column=1, sticky="ew")

        # Listbox for selected file with a scroll bar
        self.listbox_frame = ttk.Frame(self)
        self.listbox_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(10, 15))

        self.file_listbox = tk.Listbox(self.listbox_frame, selectmode=tk.SINGLE, height=10, bg="#f9f9f9", bd=0,
                                       highlightthickness=1, font=("Arial", 10))
        self.file_listbox.pack(fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)

        # Add scrollbar to the listbox
        scrollbar = ttk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Extract button
        self.extract_button = ttk.Button(self, text="Ekstrahiraj tekst", command=self.extract_text_from_file,
                                         style="Custom.TButton")
        self.extract_button.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(5, 10))

        # Initialize file path
        self.file_path = None

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

    def browse_file(self):

        file_path = filedialog.askopenfilename(title="Odaberite sliku ili PDF",
                                               filetypes=(("Image Files", "*.jpg;*.jpeg;*.png;*.bmp"),
                                                          ("PDF Files", "*.pdf")))
        if file_path:
            self.file_path = file_path
            self.update_listbox()

    def update_listbox(self):
        """Update the listbox with the selected file name."""
        self.file_listbox.delete(0, tk.END)
        if self.file_path:
            self.file_listbox.insert(tk.END, os.path.basename(self.file_path))

    def extract_text_from_file(self):
        """Extract text from the selected image or PDF."""
        if not self.file_path:
            messagebox.showwarning("Upozorenje", "Niste odabrali sliku ili PDF za ekstrakciju!")
            return

        txt_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt")])
        if txt_path:
            try:
                # Check if the file is a PDF or image
                if self.file_path.lower().endswith('.pdf'):
                    # Extract text from PDF
                    extracted_text = extract_text_from_pdf(self.file_path)
                else:
                    # Extract text from image
                    extracted_text = convert_image_to_txt(self.file_path)

                # Save the extracted text to a .txt file
                with open(txt_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(extracted_text)

                messagebox.showinfo("Uspjeh", f"Tekst je uspješno ekstrahiran: {txt_path}")

            except Exception as e:
                messagebox.showerror("Greška", str(e))
