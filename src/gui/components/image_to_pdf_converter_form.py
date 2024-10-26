import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from src.preprocessing.text_extraction import convert_images_to_txt


class ImageToTextConverterForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        # Add a title label for the section
        self.title_label = ttk.Label(self, text="Ekstrakcija teksta iz slika", font=("Helvetica", 14, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        # Label for selecting images
        self.label = ttk.Label(self, text="Odaberite slike za ekstrakciju teksta:")
        self.label.grid(row=1, column=0, columnspan=2, pady=(5, 5))

        # Entry field for folder path
        self.folder_path_entry = ttk.Entry(self)
        self.folder_path_entry.grid(row=2, column=0, sticky="ew", padx=(0, 5))
        self.folder_path_entry.insert(0, "Putanja do direktorija")

        # Button to browse images
        self.browse_button = ttk.Button(self, text="Odaberi slike", command=self.browse_images)
        self.browse_button.grid(row=2, column=1, sticky="ew")

        # Frame for listbox of selected images
        self.listbox_frame = ttk.Frame(self)
        self.listbox_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(5, 10))

        # Listbox to display selected image files
        self.image_listbox = tk.Listbox(self.listbox_frame, selectmode=tk.MULTIPLE, height=10)
        self.image_listbox.pack(fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)

        # Button to extract text from images
        self.extract_button = ttk.Button(self, text="Ekstrahiraj tekst", command=self.extract_text_from_images)
        self.extract_button.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(5, 10))

        self.image_paths = []  # Initialize an empty list for image paths

    def browse_images(self):
        file_paths = filedialog.askopenfilenames(title="Odaberite slike",
                                                 filetypes=(("Image Files", "*.jpg;*.jpeg;*.png;*.bmp"),
                                                            ("All Files", "*.*")))
        if file_paths:
            self.image_paths = list(file_paths)
            self.update_listbox()

    def update_listbox(self):
        self.image_listbox.delete(0, tk.END)  # Clear the current list
        for path in self.image_paths:
            self.image_listbox.insert(tk.END, os.path.basename(path))  # Add file names to the listbox

    def extract_text_from_images(self):
        if not self.image_paths:
            messagebox.showwarning("Upozorenje", "Niste odabrali slike za ekstrakciju!")
            return

        txt_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                  filetypes=[("Text files", "*.txt")])
        if txt_path:
            try:
                convert_images_to_txt(self.image_paths, txt_path)  # Use the new function
                messagebox.showinfo("Uspjeh", f"Tekst je uspješno ekstrapiran: {txt_path}")
            except Exception as e:
                messagebox.showerror("Greška", str(e))