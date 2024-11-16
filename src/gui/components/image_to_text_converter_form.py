import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from src.preprocessing.text_extraction import convert_images_to_txt


class ImageToTextConverterForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Configure background and padding
        self.configure(style='Custom.TFrame', padding=20)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        # Title label
        self.title_label = ttk.Label(self, text="Ekstrakcija teksta iz slika", font=("Arial", 16, "bold"),
                                     style="Custom.TLabel")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 15))

        # Directory selection label
        self.label = ttk.Label(self, text="Odaberite slike za ekstrakciju teksta:", style="Custom.TLabel")
        self.label.grid(row=1, column=0, columnspan=2, pady=(5, 10))

        # Entry for folder path
        self.folder_path_entry = ttk.Entry(self, style="Custom.TEntry")
        self.folder_path_entry.grid(row=2, column=0, sticky="ew", padx=(0, 10))
        self.folder_path_entry.insert(0, "Putanja do direktorija")

        # Browse button
        self.browse_button = ttk.Button(self, text="Odaberi slike", command=self.browse_images, style="Custom.TButton")
        self.browse_button.grid(row=2, column=1, sticky="ew")

        # Listbox for selected images with a scroll bar
        self.listbox_frame = ttk.Frame(self)
        self.listbox_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(10, 15))

        self.image_listbox = tk.Listbox(self.listbox_frame, selectmode=tk.MULTIPLE, height=10, bg="#f9f9f9", bd=0,
                                        highlightthickness=1, font=("Arial", 10))
        self.image_listbox.pack(fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)

        # Add scrollbar to the listbox
        scrollbar = ttk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL, command=self.image_listbox.yview)
        self.image_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Extract button
        self.extract_button = ttk.Button(self, text="Ekstrahiraj tekst", command=self.extract_text_from_images,
                                         style="Custom.TButton")
        self.extract_button.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(5, 10))

        # Initialize image paths
        self.image_paths = []

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

    def browse_images(self):
        """Open a file dialog to select image files."""
        file_paths = filedialog.askopenfilenames(title="Odaberite slike",
                                                 filetypes=(("Image Files", "*.jpg;*.jpeg;*.png;*.bmp"),
                                                            ("All Files", "*.*")))
        if file_paths:
            self.image_paths = list(file_paths)
            self.update_listbox()

    def update_listbox(self):
        """Update the listbox with selected image file names."""
        self.image_listbox.delete(0, tk.END)
        for path in self.image_paths:
            self.image_listbox.insert(tk.END, os.path.basename(path))

    def extract_text_from_images(self):
        """Extract text from the selected images."""
        if not self.image_paths:
            messagebox.showwarning("Upozorenje", "Niste odabrali slike za ekstrakciju!")
            return

        txt_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt")])
        if txt_path:
            try:
                convert_images_to_txt(self.image_paths, txt_path)  # Use the provided function
                messagebox.showinfo("Uspjeh", f"Tekst je uspješno ekstrahiran: {txt_path}")
            except Exception as e:
                messagebox.showerror("Greška", str(e))
