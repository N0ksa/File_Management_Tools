# config.py
import os

# Putanja do instalacije Tesseract OCR-a
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'




#Ovdje su definirani razni stilovi kako bi aplikacija bolje izgledala
def set_global_styles(style):

    style.theme_use('clam')


    style.configure(
        'Elevated.TButton',
        font=('Arial', 14, 'bold'),
        padding=12,
        relief='raised',
        borderwidth=3,
        background='#2a9d8f',
    )
    style.map(
        'Elevated.TButton',
        background=[('active', '#1b8b7f'), ('pressed', '#166d63')],
        relief=[('pressed', 'sunken')]
    )

    # Main frame background color
    style.configure('MainFrame.TFrame',
                    background="#F4F6F9")


    style.configure('Title.TLabel',
                    background="#F4F6F9",
                    foreground="#2B3A42",
                    font=('Arial', 26, 'bold'))

    # Form frame background color and padding
    style.configure('Form.TFrame',
                    background="#FFFFFF",
                    padding=20)


    style.configure('FormTitle.TLabel',
                    background="#FFFFFF",
                    foreground="#3B6B9D",
                    font=('Arial', 18, 'bold'))

    # Form buttons with subtle background and clean text
    style.configure('Form.TButton',
                    font=('Arial', 12, 'bold'),
                    background='#3B6B9D',  # Blue accent for form buttons
                    foreground='white',  # White text for contrast
                    padding=10,
                    relief="flat")  # Flat buttons for a cleaner look
    style.map('Form.TButton',
              background=[('active', '#2a7d8f'), ('pressed', '#1b6a6d')])

    # Custom entry fields with a modern, clean feel
    style.configure('Custom.TEntry',
                    font=("Arial", 16),
                    padding=(12, 14),
                    foreground="#333",  # Dark text for readability
                    background="#f8f8f8",  # Light gray for entry backgrounds
                    borderwidth=2,  # Thinner borders for a sleeker design
                    relief="sunken")

    # Progress bar customization for sleek look
    style.configure("TProgressbar",
                    thickness=20,  # Thicker progress bar for visibility
                    background="#3B6B9D",  # Blue accent for progress bar
                    troughcolor="#F4F6F9",  # Soft background color
                    )

    style.configure('Form.TLabel',
                    foreground="#000000",
                    background="#FFFFFF",
                    font=('Arial', 12, 'bold'))

