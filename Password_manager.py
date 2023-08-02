import tkinter as tk
from tkinter import simpledialog, messagebox
from cryptography.fernet import Fernet
import os

# Generate or load the encryption key
if os.path.exists("key.key"):
    with open("key.key", "rb") as key_file:
        key = key_file.read()
else:
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

cipher_suite = Fernet(key)

def encrypt_password(password):
    encrypted_password = cipher_suite.encrypt(password.encode('utf-8'))
    return encrypted_password

def decrypt_password(encrypted_password):
    decrypted_password = cipher_suite.decrypt(encrypted_password)
    return decrypted_password.decode('utf-8')

def save_password():
    dialog = PasswordInputDialog(app)
    if dialog.result is not None:
        website, username, password = dialog.result
        if website and username and password:
            encrypted_password = encrypt_password(password)
            with open("passwords.txt", "a") as password_file:
                password_file.write(f"{website} | {username} | {encrypted_password.decode('utf-8')}\n")
            messagebox.showinfo("Success", "Password saved successfully!")
        else:
            messagebox.showerror("Error", "Please fill in all the fields.")

def view_passwords():
    try:
        with open("passwords.txt", "r") as password_file:
            passwords = password_file.readlines()
        if passwords:
            decrypted_passwords = []
            for password in passwords:
                parts = password.strip().split(" | ")
                decrypted_password = f"{parts[0]} | {parts[1]} | {decrypt_password(parts[2].encode('utf-8'))}"
                decrypted_passwords.append(decrypted_password)
            show_passwords_window(decrypted_passwords)
        else:
            messagebox.showinfo("Saved Passwords", "No passwords saved yet.")
    except FileNotFoundError:
        messagebox.showinfo("Saved Passwords", "No passwords saved yet.")

def show_passwords_window(password_list):
    passwords_window = tk.Toplevel(app)
    passwords_window.title("Saved Passwords")

    listbox_passwords = tk.Listbox(passwords_window, width=50, height=10)
    listbox_passwords.pack(padx=10, pady=10)

    for password in password_list:
        listbox_passwords.insert(tk.END, password)

class PasswordInputDialog(tk.simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Website:").grid(row=0, sticky=tk.W)
        tk.Label(master, text="Username:").grid(row=1, sticky=tk.W)
        tk.Label(master, text="Password:").grid(row=2, sticky=tk.W)

        self.website_entry = tk.Entry(master)
        self.website_entry.grid(row=0, column=1)
        self.username_entry = tk.Entry(master)
        self.username_entry.grid(row=1, column=1)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.grid(row=2, column=1)

    def apply(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.result = (website, username, password)

# Create the main application window
app = tk.Tk()
app.title("Password Manager")

# Add GUI elements
button_save = tk.Button(app, text="Save Password", command=save_password)
button_save.pack(pady=10)

button_view = tk.Button(app, text="View Passwords", command=view_passwords)
button_view.pack(pady=10)

# Start the main loop
app.mainloop()
