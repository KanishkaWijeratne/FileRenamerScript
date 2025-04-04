import os
import tkinter as tk
from tkinter import filedialog, messagebox

def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_path.set(folder)
        list_files()

def list_files():
    files_listbox.delete(0, tk.END)
    try:
        for file in os.listdir(folder_path.get()):
            files_listbox.insert(tk.END, file)
    except Exception as e:
        messagebox.showerror("Error", f"Could not list files:\n{e}")

def rename_files():
    folder = folder_path.get()
    phrase = phrase_to_remove.get()
    start_trim = trim_start.get()
    end_trim = trim_end.get()

    if not folder:
        messagebox.showwarning("No folder", "Please select a folder first.")
        return

    try:
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

        for filename in files:
            name, ext = os.path.splitext(filename)
            
            # Remove specific phrase
            if phrase:
                name = name.replace(phrase, "")
            
            # Trim characters
            if start_trim.isdigit():
                name = name[int(start_trim):]
            if end_trim.isdigit():
                name = name[:-int(end_trim)] if int(end_trim) > 0 else name
            
            new_name = name + ext
            old_path = os.path.join(folder, filename)
            new_path = os.path.join(folder, new_name)

            os.rename(old_path, new_path)

        messagebox.showinfo("Success", "Files renamed successfully.")
        list_files()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to rename files:\n{e}")

# --- GUI Setup ---
root = tk.Tk()
root.title("Advanced File Renamer")

folder_path = tk.StringVar()
phrase_to_remove = tk.StringVar()
trim_start = tk.StringVar()
trim_end = tk.StringVar()

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

tk.Label(frame, text="Folder:").grid(row=0, column=0, sticky='w')
tk.Entry(frame, textvariable=folder_path, width=40).grid(row=0, column=1, padx=5)
tk.Button(frame, text="Browse", command=select_folder).grid(row=0, column=2)

tk.Label(frame, text="Phrase to remove:").grid(row=1, column=0, sticky='w')
tk.Entry(frame, textvariable=phrase_to_remove).grid(row=1, column=1, columnspan=2, sticky='we')

tk.Label(frame, text="Trim first N chars:").grid(row=2, column=0, sticky='w')
tk.Entry(frame, textvariable=trim_start, width=10).grid(row=2, column=1, sticky='w')

tk.Label(frame, text="Trim last N chars:").grid(row=3, column=0, sticky='w')
tk.Entry(frame, textvariable=trim_end, width=10).grid(row=3, column=1, sticky='w')

tk.Button(frame, text="Rename Files", command=rename_files).grid(row=4, column=1, pady=10)

files_listbox = tk.Listbox(frame, width=60, height=15)
files_listbox.grid(row=5, column=0, columnspan=3, pady=10)

root.mainloop()
