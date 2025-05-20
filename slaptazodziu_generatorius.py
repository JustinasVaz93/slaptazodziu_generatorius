import tkinter as tk
from tkinter import messagebox, filedialog
import random
import string
import os
import sys

def generate_password(length, upper, digit, punct):

    required_chars = upper + digit + punct

    if length < required_chars:
        length = required_chars

    password_chars = [random.choice(string.ascii_lowercase) for _ in range(length - required_chars)]

    password_chars.extend(random.choice(string.ascii_uppercase) for _ in range(upper))

    password_chars.extend(random.choice(string.digits) for _ in range(digit))

    password_chars.extend(random.choice(string.punctuation) for _ in range(punct))

    random.shuffle(password_chars)

    return ''.join(password_chars)


def on_generate():
    try:
        if not entry_length.get().isdigit():
            raise ValueError("Įvedėte ne skaičių arba laukelis tuščias")

        length = int(entry_length.get())
        if length < 1:
            raise ValueError("Slaptažodžio ilgis turi būti bent 1.")

        use_upper = var_upper.get()
        use_digit = var_digit.get()
        use_punct = var_punct.get()

        min_required = sum([use_upper, use_digit, use_punct])
        if length < min_required:
            raise ValueError(
                f"Slaptažodžio ilgis turi būti bent {min_required}, kad būtų galima įtraukti visus pasirinktus simbolius."
            )

        password = generate_password(length, use_upper, use_digit, use_punct)
        result_var.set(password)

    except ValueError as e:
        messagebox.showerror("Klaida", str(e))


def on_remember():
    password = result_var.get()
    if password:
        listbox_passwords.insert(tk.END, password)
    else:
        messagebox.showwarning("Įspėjimas", "Pirmiausia sugeneruokite slaptažodį.")


def on_clear():
    password = result_var.get()
    if password:
        listbox_passwords.delete(0, tk.END)
    else:
        messagebox.showwarning("Įspėjimas", "Pirmiausia sugeneruokite slaptažodį.")


def on_delete_selected():
    selected = listbox_passwords.curselection()
    if selected:
        listbox_passwords.delete(selected[0])
    else:
        messagebox.showinfo("Informacija", "Pasirinkite slaptažodį, kurį norite ištrinti.")


def on_copy_selected():
    selected = listbox_passwords.curselection()
    if selected:
        passwords = [listbox_passwords.get(i) for i in selected]
        all_passwords = "\n".join(passwords)
        pagrindinis.clipboard_clear()
        pagrindinis.clipboard_append(all_passwords)
        messagebox.showinfo("Nukopijuota", "Pasirinkti slaptažodžiai nukopijuoti.")
    else:
        messagebox.showinfo("Informacija", "Pasirinkite bent vieną slaptažodį, kurį norite kopijuoti.")


def on_save_selected():
    selected = listbox_passwords.curselection()
    if selected:
        passwords = [listbox_passwords.get(i) for i in selected]
        all_passwords = "\n".join(passwords)
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Pasirinkite kur išsaugoti slaptažodžius"
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(all_passwords)
                messagebox.showinfo("Išsaugota", "Slaptažodžiai išsaugoti sėkmingai.")
            except Exception as e:
                messagebox.showerror("Klaida", f"Nepavyko išsaugoti: {e}")
    else:
        messagebox.showinfo("Informacija", "Pasirinkite bent vieną slaptažodį, kurį norite išsaugoti.")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # kai .exe
    except Exception:
        base_path = os.path.abspath(".")  # kai .py
    return os.path.join(base_path, relative_path)


pagrindinis = tk.Tk()
pagrindinis.title("Slaptažodžių Generatorius")
pagrindinis.geometry("460x600")
pagrindinis.configure(bg="#757463")
pagrindinis.iconbitmap(resource_path("lock_icon.ico"))


label_style = {"bg": "#757463", "fg": "lightgreen"}
entry_style = {"bg": "#666556", "fg": "lightgreen", "insertbackground": "lightgreen"}
button_style = {"bg": "#757463", "fg": "black", "activebackground": "#757463"}
font_size = {"font": "6"}

tk.Label(
    pagrindinis,
    text="Slaptažodžio ilgis (Įveskite skaičių):",
    bg="#757463",
    fg="black",
    **font_size
).grid(row=2, column=0, sticky="w")

entry_length = tk.Entry(pagrindinis, **entry_style, **font_size)
entry_length.grid(row=2, column=1, padx=5, pady=5, sticky="w")

var_upper = tk.BooleanVar()
tk.Checkbutton(
    pagrindinis,
    text="Naudoti didžiąją raidę",
    bg="#757463",
    activebackground="#757463",
    variable=var_upper,
    **font_size
).grid(row=3, columnspan=2, sticky="w")

var_digit = tk.BooleanVar()
tk.Checkbutton(
    pagrindinis,
    text="Naudoti skaičių",
    bg="#757463",
    activebackground="#757463",
    variable=var_digit,
    **font_size
).grid(row=4, columnspan=2, sticky="w")

var_punct = tk.BooleanVar()
tk.Checkbutton(
    pagrindinis,
    text="Naudoti simbolį",
    bg="#757463",
    activebackground="#757463",
    variable=var_punct,
    **font_size
).grid(row=5, columnspan=2, sticky="w")

tk.Button(
    pagrindinis,
    text="Generuoti",
    command=on_generate,
    **button_style,
    **font_size
).grid(row=6, columnspan=4, pady=5, sticky="ns")

result_var = tk.StringVar()
tk.Entry(
    pagrindinis,
    textvariable=result_var,
    width=35,
    bg="#666556",
    fg="lightgreen",
    insertbackground= "lightgreen",
    **font_size
).grid(row=7, columnspan=4, pady=5)

tk.Button(
    pagrindinis,
    text="Atsiminti slaptažodį",
    command=on_remember,
    **button_style,
    **font_size
).grid(row=8, column=0, pady=5, sticky="ns")

tk.Label(
    pagrindinis,
    text="Atsiminti slaptažodžiai:",
    bg="#757463",
    **font_size
).grid(row=9, column=0, sticky="s", pady=(10, 0))

listbox_passwords = tk.Listbox(
    pagrindinis,
    width=35,
    bg="#666556",
    fg="lightgreen",
    selectmode="extended",
    selectbackground= "#757463",
    selectforeground= "lightgreen",
    **font_size
)
listbox_passwords.grid(row=10, columnspan=5, padx=5, pady=5)

tk.Button(
    pagrindinis,
    text="       Ištrinti visus      ",
    command=on_clear,
    **button_style,
    **font_size
).grid(row=11, column=0, padx=5, pady=5,sticky="ns")

tk.Button(
    pagrindinis,
    text="Ištrinti pasirinktą",
    command=on_delete_selected,
    **button_style,
    **font_size
).grid(row=11, column=1, padx=5, pady=5, sticky="ns")

tk.Button(
    pagrindinis,
    text="Kopijuoti pasirinktą",
    command=on_copy_selected,
    **button_style,
    **font_size
).grid(row=12, column=0, padx=5, pady=5, sticky="ns")

tk.Button(
    pagrindinis,
    text=" Išsaugoti į failą ",
    command=on_save_selected,
    **button_style,
    **font_size
).grid(row=12, column=1, padx=5, pady=5, sticky="ns")

pagrindinis.mainloop()
