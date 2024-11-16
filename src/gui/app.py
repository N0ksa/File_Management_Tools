import tkinter as tk
from tkinter import ttk
from src.gui.components.image_to_pdf_form import ImageToPdfForm
from src.gui.components.to_text_converter_form import ImageToTextConverterForm
from src.gui.components.pdf_mover_form import PdfMoverForm
from src.gui.components.pdf_renamer_form import PdfRenamerForm


def main():
    app = Application()
    app.mainloop()


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Management Tools")
        self.geometry("800x600")
        self.configure(bg="#264653")  # Deep teal background for the main window

        # Style configuration for the buttons
        style = ttk.Style(self)
        style.configure(
            'Elevated.TButton',
            font=('Arial', 14, 'bold'),
            padding=15,
            relief='raised',
            borderwidth=5,
            background='#2a9d8f',  # Muted greenish-blue
        )
        style.map(
            'Elevated.TButton',
            background=[('active', '#1b8b7f'),  # Darker green on hover
                        ('pressed', '#166d63')],  # Even darker green on click
        )

        # Create and configure the style for the main frame
        self.style = ttk.Style()
        self.style.configure('MainFrame.TFrame', background="#e9c46a")  # Light yellow for contrast

        # Layout configuration
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Main frame with padding
        self.main_frame = ttk.Frame(self, style='MainFrame.TFrame', padding=20)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)

        # Title label
        self.title_label = ttk.Label(
            self.main_frame,
            text="File Management Tools",
            font=('Arial', 24, 'bold'),
            anchor="center",
            background="#e9c46a",  # Match the frame background
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Buttons with consistent styling
        self.create_buttons()

    def create_buttons(self):
        """Create the main navigation buttons."""
        buttons = [
            ("Otvori PDF Renamer", self.open_pdf_renamer),
            ("Otvori PDF Mover", self.open_pdf_mover),
            ("Otvori Image to PDF", self.open_image_to_pdf),  # Moved to appear before Text Extractor
            ("Otvori Text Extractor", self.open_pdf_converter),  # Moved to appear after Image to PDF
        ]

        for idx, (text, command) in enumerate(buttons):
            row, col = divmod(idx, 2)  # Determine row and column
            button = ttk.Button(self.main_frame, text=text, command=command, style='Elevated.TButton')
            button.grid(row=row + 1, column=col, sticky="nsew", padx=20, pady=20)

    def open_pdf_renamer(self):
        self.open_new_window(PdfRenamerForm, "PDF Renamer")

    def open_pdf_mover(self):
        self.open_new_window(PdfMoverForm, "PDF Mover")

    def open_pdf_converter(self):
        self.open_new_window(ImageToTextConverterForm, "PDF Converter")

    def open_image_to_pdf(self):
        self.open_new_window(ImageToPdfForm, "Image to PDF")

    def open_new_window(self, form_class, title):
        """Open a new window with the provided form class."""
        new_window = tk.Toplevel(self)
        new_window.title(title)
        new_window.geometry("700x500")
        new_window.configure(bg="#f4a261")  # Light orange for the new window background

        # Create a frame in the new window
        padded_frame = ttk.Frame(new_window, style='MainFrame.TFrame', padding=20)
        padded_frame.pack(fill=tk.BOTH, expand=True)

        # Add the form to the frame
        form_class(padded_frame).pack(fill=tk.BOTH, expand=True)

        # Set modal behavior
        new_window.grab_set()
        new_window.focus_set()
        new_window.transient(self)


if __name__ == "__main__":
    main()
