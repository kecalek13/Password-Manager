import tkinter as tk
from tkinter import ttk
import pickle
import secrets
import string

class PasswordManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Správce hesel")
        self.master.resizable(False,False)

        # Načtení existujících hesel nebo vytvoření nového seznamu
        try:
            with open("passwords.pkl", "rb") as file:
                self.passwords = pickle.load(file)
        except FileNotFoundError:
            self.passwords = []

        # Nadpis
        title_label = ttk.Label(master, text="Správce hesel", font=('Helvetica', 16))
        title_label.grid(row=0, column=0, columnspan=5, pady=10)

        # Uživatelské jméno
        username_label = ttk.Label(master, text="Uživatelské jméno:")
        username_label.grid(row=1, column=0, padx=10)
        self.username_entry = ttk.Entry(master)
        self.username_entry.grid(row=1, column=1, padx=10)

        # Heslo
        password_label = ttk.Label(master, text="Heslo:")
        password_label.grid(row=2, column=0, padx=10)
        self.password_entry = ttk.Entry(master, show="*")
        self.password_entry.grid(row=2, column=1, padx=10)

        # Tlačítko pro zobrazení/ukrytí hesla
        show_password_button = ttk.Button(master, text="Zobrazit heslo", command=self.toggle_password_visibility)
        show_password_button.grid(row=2, column=2, padx=10)

        # Tlačítko pro ukládání hesla
        save_button = ttk.Button(master, text="Uložit heslo", command=self.save_password)
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Tlačítko pro smazání všech hesel
        delete_all_button = ttk.Button(master, text="Smazat všechna hesla", command=self.delete_all_passwords)
        delete_all_button.grid(row=3, column=2, pady=10)

        # Tlačítko pro generování hesla
        generate_button = ttk.Button(master, text="Generovat heslo", command=self.generate_password)
        generate_button.grid(row=3, column=3, pady=10)

        # Textové pole pro zobrazení hesel
        self.password_display = tk.Text(master, height=10, width=40)
        self.password_display.grid(row=4, column=0, columnspan=4, pady=10)

        # Aktualizace zobrazení při spuštění
        self.update_display()

        # Uložení hesel při zavření okna
        master.protocol("WM_DELETE_WINDOW", self.on_close)

    def save_password(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            self.passwords.append({"Username": username, "Password": password})
            self.update_display()
            self.save_to_file()
        else:
            print("Vyplňte uživatelské jméno a heslo.")

    def delete_all_passwords(self):
        self.passwords = []
        self.update_display()
        self.save_to_file()

    def generate_password(self):
        password_length = 12
        characters = string.ascii_letters + string.digits + string.punctuation
        generated_password = ''.join(secrets.choice(characters) for _ in range(password_length))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, generated_password)

    def toggle_password_visibility(self):
        current_show_state = self.password_entry.cget("show")
        new_show_state = "" if current_show_state else "*"
        self.password_entry.config(show=new_show_state)

    def update_display(self):
        self.password_display.delete(1.0, tk.END)  # Vymaže obsah textového pole

        for entry in self.passwords:
            self.password_display.insert(tk.END, f"Username: {entry['Username']}\nPassword: {entry['Password']}\n\n")

    def save_to_file(self):
        with open("passwords.pkl", "wb") as file:
            pickle.dump(self.passwords, file)

    def on_close(self):
        self.save_to_file()
        self.master.destroy()

# Vytvoření hlavního okna
root = tk.Tk()
app = PasswordManager(root)

# Spuštění hlavní smyčky Tkinteru
root.mainloop()
