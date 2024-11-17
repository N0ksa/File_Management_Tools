import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.pdf_moving.pdf_mover import PdfMover
import threading



class PdfMoverForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(style='Custom.TFrame', padding=20)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)

        self.title_label = ttk.Label(self, text="Premještanje PDF datotekama", font=("Arial", 16, "bold"),
                                     style="Custom.TLabel")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 15))

        self.label = ttk.Label(self, text="Odaberite direktorij s PDF datotekama:", style="Custom.TLabel")
        self.label.grid(row=1, column=0, columnspan=2, pady=(5, 10))

        self.folder_path_entry = ttk.Entry(self, style="Custom.TEntry")
        self.folder_path_entry.grid(row=2, column=0, sticky="ew", padx=(0, 10))
        self.folder_path_entry.insert(0, "Putanja do direktorija")

        self.browse_button = ttk.Button(self, text="Odaberi direktorij", command=self.browse_folder,
                                        style="Custom.TButton")
        self.browse_button.grid(row=2, column=1, sticky="ew")

        self.destination_path_entry = ttk.Entry(self, style="Custom.TEntry")
        self.destination_path_entry.grid(row=3, column=0, sticky="ew", padx=(0, 10))
        self.destination_path_entry.insert(0, "Putanja do odredišne mape")

        self.destination_button = ttk.Button(self, text="Odaberi odredišnu mapu",
                                             command=self.select_destination_folder,
                                             style="Custom.TButton")
        self.destination_button.grid(row=3, column=1, sticky="ew", pady=(5, 10))

        self.listbox_frame = ttk.Frame(self)
        self.listbox_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=(10, 15))

        self.file_listbox = tk.Listbox(self.listbox_frame, selectmode=tk.MULTIPLE, height=10, bg="#f9f9f9", bd=0,
                                       highlightthickness=1, font=("Arial", 10))
        self.file_listbox.pack(fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)


        self.move_button = ttk.Button(self, text="Premjesti PDF", command=self.start_move_pdfs_thread,
                                      style="Custom.TButton")
        self.move_button.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(5, 10))


        self.progressbar = ttk.Progressbar(self, orient="horizontal", mode="indeterminate", length=300)
        self.progressbar.grid(row=6, column=0, columnspan=2, pady=(10, 15))
        self.progressbar.grid_remove()  # Hide progress bar initially


        self.set_styles()

    def set_styles(self):
        style = ttk.Style()
        style.configure('Custom.TFrame', background='#fefae0')  # Ivory
        style.configure('Custom.TLabel', background='#fefae0', font=('Arial', 14), foreground='#34495e')  # Slate Gray
        style.configure('Custom.TButton', font=('Arial', 12), padding=10, background='#4caf50')  # Green
        style.map('Custom.TButton', background=[('active', '#388e3c'), ('pressed', '#2e7d32')])  # Darker green
        style.configure('Custom.TEntry', fieldbackground='#ffffff', bordercolor='#34495e', padding=10,
                        font=('Arial', 12))

    def browse_folder(self):
        folder_path = filedialog.askdirectory(title="Odaberite direktorij s PDF datotekama")
        if folder_path:
            self.folder_path_entry.delete(0, tk.END)
            self.folder_path_entry.insert(0, folder_path)
            self.load_pdf_files(folder_path)

    def load_pdf_files(self, folder_path):
        self.file_listbox.delete(0, tk.END)
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
        self.pdf_files = [os.path.join(folder_path, f) for f in pdf_files]
        for pdf_file in pdf_files:
            self.file_listbox.insert(tk.END, pdf_file)

    def select_destination_folder(self):
        folder_path = filedialog.askdirectory(title="Odaberite odredišnu mapu")
        if folder_path:
            self.destination_folder = folder_path
            self.destination_path_entry.delete(0, tk.END)
            self.destination_path_entry.insert(0, folder_path)
            messagebox.showinfo("Odabrana mapa", f"Odabrana odredišna mapa: {self.destination_folder}")

    def start_move_pdfs_thread(self):

        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Upozorenje", "Molimo odaberite PDF datoteke za premještanje.")
            return

        self.move_button.config(state=tk.DISABLED)

        thread = threading.Thread(target=self.move_selected_pdfs)
        thread.start()

    def move_selected_pdfs(self):
        if not hasattr(self, 'destination_folder') or not self.destination_folder:
            self.after(0, lambda: messagebox.showwarning("Upozorenje", "Niste odabrali odredišnu mapu."))
            self.after(0, lambda: self.move_button.config(state=tk.NORMAL))  # Ponovno aktiviraj gumb
            return

        if not self.pdf_files:
            self.after(0, lambda: messagebox.showwarning("Upozorenje", "Niste učitali PDF datoteke."))
            self.after(0, lambda: self.move_button.config(state=tk.NORMAL))  # Ponovno aktiviraj gumb
            return

        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            self.after(0,
                       lambda: messagebox.showwarning("Upozorenje", "Molimo odaberite PDF datoteke za premještanje."))
            self.after(0, lambda: self.move_button.config(state=tk.NORMAL))  # Ponovno aktiviraj gumb
            return

        pdf_files_to_move = [self.pdf_files[index] for index in selected_indices]
        pdf_mover = PdfMover(self.destination_folder)

        success_count = 0
        failure_count = 0

        self.after(0, lambda: self.progressbar.grid())
        self.after(0, lambda: self.progressbar.start())

        for pdf_path in pdf_files_to_move:
            result = pdf_mover.process_and_move_pdf(pdf_path)
            if result:
                success_count += 1
            else:
                failure_count += 1

        self.after(0, lambda: self.progressbar.stop())
        self.after(0, lambda: self.progressbar.grid_remove())
        self.after(0, lambda: self.move_button.config(state=tk.NORMAL))

        if success_count == 0:
            self.after(0, lambda: messagebox.showerror("Greška", "Nijedan PDF nije uspješno premješten. Za više informacija pogledaj log."))
        else:
            self.after(0, lambda: messagebox.showinfo(
                "Uspjeh",
                f"Premještanje završeno.\n"
                f"Uspješno premješteno: {success_count}\n"
                f"Neuspješno premješteno: {failure_count}."
            ))


        self.after(0, lambda: self.load_pdf_files(self.folder_path_entry.get()))
