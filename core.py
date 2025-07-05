import os
import secrets
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import zipfile
import shutil
import tempfile

# Shred a single file securely
def shred_file(filepath, passes):
    try:
        filesize = os.path.getsize(filepath)
        with open(filepath, 'ba+', buffering=0) as f:
            for _ in range(passes):
                f.seek(0)
                f.write(secrets.token_bytes(filesize))
        os.remove(filepath)
        return True
    except Exception as e:
        print(f"[ERROR] Failed to shred {filepath}: {e}")
        return False

# Zip a folder and shred the resulting .zip
def zip_and_shred_folder(folder_path, passes):
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "shred_me.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        arc_path = os.path.relpath(full_path, folder_path)
                        zipf.write(full_path, arc_path)
            shred_file(zip_path, passes)
        return True
    except Exception as e:
        print(f"[ERROR] Folder zip/shred failed: {e}")
        return False

# Handler for multi-file shredding
def handle_files():
    paths = filedialog.askopenfilenames(title="Select Files to Shred")
    if not paths:
        return
    passes = simpledialog.askinteger("Overwrite Passes", "Enter passes (e.g. 7, 35):", minvalue=1, maxvalue=100)
    if not passes:
        return
    for path in paths:
        shred_file(path, passes)
    messagebox.showinfo("✅ Done", "Selected files shredded.")

# Handler for folder shred
def handle_folder():
    folder = filedialog.askdirectory(title="Select Folder to Zip & Shred")
    if not folder:
        return
    passes = simpledialog.askinteger("Overwrite Passes", "Enter passes (e.g. 7, 35):", minvalue=1, maxvalue=100)
    if not passes:
        return
    if zip_and_shred_folder(folder, passes):
        messagebox.showinfo("✅ Done", f"Folder zipped and shredded.")

# GUI setup
root = tk.Tk()
root.title("DarkShred Ultimate")
root.configure(bg="#1e1e1e")

tk.Button(root, text="🗑️ Shred Files", command=handle_files,
          bg="#2d2d2d", fg="#ffffff", font=("Segoe UI", 12, "bold")).pack(padx=30, pady=(30,10))

tk.Button(root, text="📦 Shred Folder (Zip First)", command=handle_folder,
          bg="#2d2d2d", fg="#ffffff", font=("Segoe UI", 12, "bold")).pack(padx=30, pady=(10,30))

root.mainloop()
