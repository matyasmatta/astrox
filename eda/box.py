import tkinter as tk
from tkinter import messagebox

def show_message():
    messagebox.showinfo("Výzva", "Toto je zpráva.")

# Vytvoření hlavního okna
window = tk.Tk()

# Vytvoření tlačítka
button = tk.Button(window, text="Zobrazit zprávu", command=show_message)
button.pack()

# Spuštění smyčky hlavního okna
window.mainloop()