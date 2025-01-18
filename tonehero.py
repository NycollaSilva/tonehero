import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO

class ModernChordLibraryApp:
    def __init__(self, root):
        self.bg_color = "#000000"  # Black background
        self.fg_color = "#00aaff"  # Blue foreground

        self.root = root
        root.title("Biblioteca de Acordes Moderna")
        root.configure(bg=self.bg_color)

        # Estilo personalizado
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color)
        style.configure("TCombobox", selectbackground=self.bg_color, fieldbackground="white", foreground=self.fg_color)
        style.configure("TScrollbar", background=self.bg_color, troughcolor=self.fg_color)
        style.configure("TButton", background=self.bg_color, foreground=self.fg_color, focuscolor=self.bg_color)
        style.map("TButton",
                  background=[("active", self.fg_color)],
                  foreground=[("active", self.bg_color)])

        # Defina a interface principal
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Adicione o título
        self.title_label = ttk.Label(self.main_frame, text="Biblioteca de Acordes", font=("Helvetica", 18, "bold"))
        self.title_label.grid(row=0, column=0, pady=(0, 10), columnspan=2)

        # Botões de selecionar categoria
        self.category_label = ttk.Label(self.main_frame, text="Selecione a Categoria:", font=("Arial", 12, "bold"))
        self.category_label.grid(row=1, column=0, pady=10)

        self.category_var = tk.StringVar()
        self.category_frame = ttk.Frame(self.main_frame)
        self.category_frame.grid(row=1, column=1, pady=10)

        self.major_button = ttk.Button(self.category_frame, text="Maiores", command=lambda: self.load_chords("Maiores"))
        self.minor_button = ttk.Button(self.category_frame, text="Menores", command=lambda: self.load_chords("Menores"))

        self.major_button.pack(side="left", padx=5)
        self.minor_button.pack(side="left", padx=5)

        # Lista que mostra os acordes
        self.chord_listbox = tk.Listbox(self.main_frame, height=15, width=30, font=("Arial", 12), bg=self.bg_color, fg=self.fg_color)
        self.chord_listbox.grid(row=2, column=0, padx=(0, 20), pady=(0, 20), sticky="ns")

        # Scrollbar para Listbox
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.chord_listbox.yview)
        self.chord_listbox.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=2, column=1, sticky="nsw")

        # Placeholder para exibir detalhes dos acordes
        self.chord_details_frame = ttk.Frame(self.main_frame, padding="10")
        self.chord_details_frame.grid(row=2, column=2, pady=(0, 20))

        # Mostrar detalhes do acorde selecionado
        self.chord_listbox.bind('<<ListboxSelect>>', self.show_chord_details)

        # Dicionário de acordes
        self.chords = {
            "Maiores": {
                "C Major": "https://chordbank.com/cb4dg/cagey_dani_1_750.png",
                "G Major": "https://chordbank.com/cb4dg/notable_cora_1_750.png",
                "D Major": "https://chordbank.com/cb4dg/acidic_mel_1_750.png",
                "A Major": "https://chordbank.com/cb4dg/artful_mae_1_750.png",
                "E Major": "https://chordbank.com/cb4dg/earthy_ian_1_750.png",
                "F Major": "https://chordbank.com/cb4dg/grumpy_lulu_1_750.png",
            },
            "Menores": {
                "A Minor": "https://chordbank.com/cb4dg/artful_luigi_1_750.png",
                "E Minor": "https://chordbank.com/cb4dg/earthy_clo_1_750.png",
                "D Minor": "https://chordbank.com/cb4dg/acidic_mei_1_750.png",
                "G Minor": "https://chordbank.com/cb4dg/grumpy_isa_3_750.png",
                "C Minor": "https://chordbank.com/cb4dg/bestial_sam_3_750.png",
                "F Minor": "https://chordbank.com/cb4dg/grumpy_isa_1_750.png",
            }
        }

    def load_chords(self, category):
        self.chord_listbox.delete(0, tk.END)
        for chord in self.chords[category]:
            self.chord_listbox.insert(tk.END, chord)

    def show_chord_details(self, event):
        selected_index = self.chord_listbox.curselection()
        if selected_index:
            category = self.category_var.get()
            chord_name = self.chord_listbox.get(selected_index)
            chord_image_url = self.chords[category][chord_name]

            try:
                response = requests.get(chord_image_url)
                response.raise_for_status()
                image_data = response.content
                chord_image = Image.open(BytesIO(image_data))
                chord_image.thumbnail((300, 300))
                photo = ImageTk.PhotoImage(chord_image)

                # Limpar frame antes de inserir novo detalhe
                for widget in self.chord_details_frame.winfo_children():
                    widget.destroy()

                ttk.Label(self.chord_details_frame, text=f"Acorde: {chord_name}", font=("Helvetica", 16, "bold")).grid(row=0, column=0)

                image_label = ttk.Label(self.chord_details_frame, image=photo)
                image_label.image = photo  # Manter referência da imagem para evitar garbage collection
                image_label.grid(row=1, column=0)
            except requests.exceptions.RequestException as e:
                print(f"Erro ao carregar a imagem do diagrama: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernChordLibraryApp(root)
    root.geometry("800x600")
    root.mainloop()
