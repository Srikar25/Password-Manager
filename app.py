import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip
import password_db

def generate_password():
    """Generate a strong password based on user-defined constraints."""
    try:
        app_name = app_name_entry.get().strip()
        min_length = int(min_length_entry.get())
        max_length = int(max_length_entry.get())
        special_chars = special_chars_entry.get()

        if not app_name:
            messagebox.showerror("Error", "Please enter the application name!")
            return
        if min_length > max_length:
            messagebox.showerror("Error", "Min length cannot be greater than max length!")
            return

        char_pool = string.digits
        if uppercase_var.get():
            char_pool += string.ascii_uppercase
        if lowercase_var.get():
            char_pool += string.ascii_lowercase
        char_pool += special_chars

        if not char_pool:
            messagebox.showerror("Error", "No valid character set selected!")
            return

        password = []
        if uppercase_var.get():
            password.append(random.choice(string.ascii_uppercase))
        if lowercase_var.get():
            password.append(random.choice(string.ascii_lowercase))
        if special_chars:
            password.append(random.choice(special_chars))

        remaining_length = random.randint(min_length, max_length) - len(password)
        password.extend(random.choices(char_pool, k=remaining_length))
        random.shuffle(password)

        final_password = "".join(password)
        password_output.set(final_password)

        password_db.save_password(app_name, final_password)
        messagebox.showinfo("Success", f"Password saved for {app_name}!")
        refresh_passwords()

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for min/max length.")

def refresh_passwords(search_query=""):
    """Fetch and display only application names."""
    for row in password_table.get_children():
        password_table.delete(row)

    saved_apps = password_db.get_saved_apps(search_query)
    for app in saved_apps:
        password_table.insert("", "end", values=(app,))

def delete_password():
    """Delete selected password entry from database."""
    selected_item = password_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select an application to delete!")
        return

    app_name = password_table.item(selected_item, "values")[0]
    password_db.delete_password(app_name)
    messagebox.showinfo("Deleted", f"Password for {app_name} deleted.")
    refresh_passwords()

def show_decrypted_password(event):
    """Decrypt and display the password when clicking an application name."""
    selected_item = password_table.selection()
    if not selected_item:
        return

    app_name = password_table.item(selected_item, "values")[0]
    decrypted_password = password_db.get_decrypted_password(app_name)

    if decrypted_password:
        messagebox.showinfo("Decrypted Password", f"Password for {app_name}: {decrypted_password}")
        pyperclip.copy(decrypted_password)  # Copy to clipboard
    else:
        messagebox.showerror("Error", "Failed to retrieve password.")

def search_passwords():
    """Search applications based on user input."""
    search_query = search_entry.get()
    refresh_passwords(search_query)

# Tkinter GUI setup
root = tk.Tk()
root.title("Password Manager")
root.geometry("500x400")

notebook = ttk.Notebook(root)
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
notebook.add(tab1, text="Generate Password")
notebook.add(tab2, text="View Saved Applications")
notebook.pack(expand=True, fill="both")

# Tab 1: Password Generator
tk.Label(tab1, text="Application Name:").pack()
app_name_entry = tk.Entry(tab1)
app_name_entry.pack()

uppercase_var = tk.BooleanVar()
lowercase_var = tk.BooleanVar()
tk.Checkbutton(tab1, text="At least 1 Uppercase Letter", variable=uppercase_var).pack(anchor="w")
tk.Checkbutton(tab1, text="At least 1 Lowercase Letter", variable=lowercase_var).pack(anchor="w")

tk.Label(tab1, text="Min Characters:").pack()
min_length_entry = tk.Entry(tab1)
min_length_entry.pack()

tk.Label(tab1, text="Max Characters:").pack()
max_length_entry = tk.Entry(tab1)
max_length_entry.pack()

tk.Label(tab1, text="Allowed Special Characters:").pack()
special_chars_entry = tk.Entry(tab1)
special_chars_entry.pack()

tk.Button(tab1, text="Generate Password", command=generate_password).pack(pady=5)

password_output = tk.StringVar()
tk.Label(tab1, text="Generated Password:").pack()
tk.Entry(tab1, textvariable=password_output, state="readonly", width=30).pack()

# Tab 2: View Saved Applications
search_entry = tk.Entry(tab2)
search_entry.pack()
tk.Button(tab2, text="Search", command=search_passwords).pack()

password_table = ttk.Treeview(tab2, columns=("App Name",), show="headings")
password_table.heading("App Name", text="Application")
password_table.pack(expand=True, fill="both")
password_table.bind("<Double-1>", show_decrypted_password)  # Double-click to show password

tk.Button(tab2, text="Delete Selected", command=delete_password).pack(pady=5)

refresh_passwords()
root.mainloop()
