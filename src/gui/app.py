import tkinter as tk
from tkinter import ttk
from src.gui.components.image_to_pdf_form import ImageToPdfForm
from src.gui.components.to_text_converter_form import TextConverterForm
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
        self.configure(bg="#F7F7F7")

        # Prevent resizing of the main window
        self.resizable(width=False, height=False)
        self.minsize(800, 600)

        # Set the application icon
        self.iconphoto(False, tk.PhotoImage(file="../../resources/icons/main_icon.png"))

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
        self.style.configure('MainFrame.TFrame', background="#F7F7F7")

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
            background="#F7F7F7",
            foreground="#3B6B9D",
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Buttons with consistent styling
        self.create_buttons()

    def create_buttons(self):
        """Create the main navigation buttons."""
        # Load icons and resize them by scaling down (subsample)
        self.pdf_renamer_icon = tk.PhotoImage(file="../../resources/icons/pdf_renamer.png").subsample(6, 6)
        self.pdf_mover_icon = tk.PhotoImage(file="../../resources/icons/pdf_mover.png").subsample(5, 5)
        self.image_to_pdf_icon = tk.PhotoImage(file="../../resources/icons/image_scanner.png").subsample(6, 6)
        self.text_extractor_icon = tk.PhotoImage(file="../../resources/icons/text_extraction.png").subsample(6, 6)

        buttons = [
            ("PDF Renamer", self.open_pdf_renamer, self.pdf_renamer_icon),
            ("PDF Mover", self.open_pdf_mover, self.pdf_mover_icon),
            ("Image to PDF", self.open_image_to_pdf, self.image_to_pdf_icon),
            ("Text Extractor", self.open_pdf_converter, self.text_extractor_icon),
        ]

        for idx, (text, command, icon) in enumerate(buttons):
            row, col = divmod(idx, 2)  # Determine row and column
            button = ttk.Button(self.main_frame, text=text, command=command, style='Elevated.TButton', image=icon, compound=tk.BOTTOM)
            # Added padding at the bottom of the text
            button.grid(row=row + 1, column=col, sticky="nsew", padx=20, pady=(20, 20))  # More padding at the bottom

    def open_pdf_renamer(self):
        self.open_new_window(PdfRenamerForm, "PDF Renamer")

    def open_pdf_mover(self):
        self.open_new_window(PdfMoverForm, "PDF Mover")

    def open_pdf_converter(self):
        self.open_new_window(TextConverterForm, "PDF Converter")

    def open_image_to_pdf(self):
        self.open_new_window(ImageToPdfForm, "Image to PDF")

    def open_new_window(self, form_class, title):
        """Open a new window with the provided form class."""
        new_window = tk.Toplevel(self)
        new_window.title(title)
        new_window.geometry("700x500")
        new_window.configure(bg="#f4a261")  # Light orange for the new window background

        # Prevent resizing for the new window
        new_window.resizable(width=False, height=False)

        # Set the new window icon (optional, same as main)
        new_window.iconphoto(False, tk.PhotoImage(file="../../resources/icons/main_icon.png"))

        # Center the new window on the main window
        self.center_window(new_window)

        # Create a frame in the new window
        padded_frame = ttk.Frame(new_window, style='MainFrame.TFrame', padding=20)
        padded_frame.pack(fill=tk.BOTH, expand=True)

        # Add the form to the frame
        form_class(padded_frame).pack(fill=tk.BOTH, expand=True)

        # Set modal behavior
        new_window.grab_set()
        new_window.focus_set()
        new_window.transient(self)

    def center_window(self, window):
        """Center the window relative to the main window."""
        window.update_idletasks()  # Ensure that window's geometry is up to date
        width = window.winfo_width()
        height = window.winfo_height()

        # Get the position of the main window
        main_window_x = self.winfo_x()
        main_window_y = self.winfo_y()

        # Get the width and height of the main window
        main_window_width = self.winfo_width()
        main_window_height = self.winfo_height()

        # Calculate position for centering the new window relative to the main window
        position_left = main_window_x + (main_window_width // 2) - (width // 2)
        position_top = main_window_y + (main_window_height // 2) - (height // 2)

        # Set the position of the new window
        window.geometry(f'{width}x{height}+{position_left}+{position_top}')


if __name__ == "__main__":
    main()
