import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_label.config(text=f"📁 Selected Folder:\n{folder_path}", fg="black")
    else:
        folder_label.config(text="❌ No folder selected", fg="red")

# Create main window
root = tk.Tk()
root.title("📂 Folder Upload")
root.geometry("600x350")
root.configure(bg="#E8F0FE")

# Style
style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 12), padding=10)

# Title label
title = tk.Label(root, text="✨ Upload a Folder", font=("Segoe UI", 18, "bold"),
                 bg="#E8F0FE", fg="#1A73E8")
title.pack(pady=20)

# Upload Button
upload_btn = ttk.Button(root, text="📤 Browse Folder", command=select_folder)
upload_btn.pack(pady=10)

# Folder display
folder_label = tk.Label(root, text="No folder selected yet...", font=("Segoe UI", 12),
                        bg="#E8F0FE", fg="gray", wraplength=500, justify="center")
folder_label.pack(pady=20)

# Exit button
exit_btn = ttk.Button(root, text="❌ Exit", command=root.destroy)
exit_btn.pack(pady=10)

# Run the app
root.mainloop()
