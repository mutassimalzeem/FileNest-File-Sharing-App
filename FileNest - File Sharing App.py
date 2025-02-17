import os
import socket
import threading
import tkinter as tk
from tkinter import ttk, filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
import http.server
import socketserver
import webbrowser
import pyqrcode
import json, png
import shutil

# Global variables
current_theme = "light"
themes = {
    "light": {"bg": "white", "fg": "black", "button_bg": "#f0f0f0", "button_fg": "black"},
    "dark": {"bg": "#1c1c1c", "fg": "white", "button_bg": "#333333", "button_fg": "white"}
}
shared_files = []
SHARED_DIR = "./shared_files"

# Function to toggle themes
def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    theme = themes[current_theme]
    root.config(bg=theme["bg"])
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
            widget.config(bg=theme["bg"], fg=theme["fg"])
        elif isinstance(widget, tk.Frame):
            widget.config(bg=theme["bg"])
        elif isinstance(widget, tk.Listbox):
            widget.config(bg=theme["bg"], fg=theme["fg"])

# Function to handle file drop
def on_drop(event):
    file_paths = event.data.strip('{}').split()  # Handle multiple files
    for file_path in file_paths:
        if file_path and file_path not in shared_files:
            shared_files.append(file_path)
    update_file_list()
    if file_paths:
        preview_file(file_paths[0])  # Preview the first file

# Function to browse and select files
def browse_files():
    file_paths = filedialog.askopenfilenames(title="Select Files")
    for file_path in file_paths:
        if file_path and file_path not in shared_files:
            shared_files.append(file_path)
    update_file_list()
    if file_paths:
        preview_file(file_paths[0])  # Preview the first selected file

# Function to update the list of shared files
def update_file_list():
    file_listbox.delete(0, tk.END)
    for file_path in shared_files:
        file_listbox.insert(tk.END, os.path.basename(file_path))

# Function to preview the dropped file
def preview_file(file_path):
    try:
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            img = Image.open(file_path)
            img.thumbnail((150, 150))  # Resize for preview
            img_tk = ImageTk.PhotoImage(img)
            preview_label.config(image=img_tk)
            preview_label.image = img_tk
        elif file_path.lower().endswith('.txt'):
            with open(file_path, 'r') as f:
                content = f.read(100)  # Read first 100 characters
            preview_label.config(text=content, image=None)
        else:
            preview_label.config(text="Preview not available for this file type.", image=None)
    except Exception as e:
        preview_label.config(text=f"Error loading preview: {e}", image=None)

# Function to organize files into folders
def create_folder():
    folder_name = folder_entry.get()
    if folder_name:
        os.makedirs(folder_name, exist_ok=True)
        for file_path in shared_files:
            shutil.move(file_path, os.path.join(folder_name, os.path.basename(file_path)))
        shared_files.clear()
        update_file_list()

# Save user preferences (theme)
def save_preferences():
    preferences = {"theme": current_theme}
    with open("preferences.json", "w") as f:
        json.dump(preferences, f)

# Load user preferences
def load_preferences():
    global current_theme
    try:
        with open("preferences.json", "r") as f:
            preferences = json.load(f)
            current_theme = preferences.get("theme", "light")
    except FileNotFoundError:
        pass

# Start the HTTP server
PORT = 8010
def start_http_server():
    os.makedirs(SHARED_DIR, exist_ok=True)
    for file_path in shared_files:
        shutil.copy(file_path, SHARED_DIR)
    os.chdir(SHARED_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

def start_server_thread():
    server_thread = threading.Thread(target=start_http_server, daemon=True)
    server_thread.start()

# Generate QR Code
def generate_qr_code():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    link = f"http://{ip_address}:{PORT}"
    url = pyqrcode.create(link)
    url.png("qrcode.png", scale=6)
    return link

# Display QR Code
def show_qr_code():
    link = generate_qr_code()
    qr_label.config(text=f"Scan this QR Code:\n{link}")
    webbrowser.open("qrcode.png")

# Main application setup
root = TkinterDnD.Tk()
root.title("File Sharing App")
root.geometry("500x800")

# Load preferences
load_preferences()

# Apply initial theme
toggle_theme()

# Header Label
header_label = tk.Label(root, text="Drag and Drop Files Here", font=("Arial", 16), bg=themes[current_theme]["bg"], fg=themes[current_theme]["fg"])
header_label.pack(pady=10)

# Drop Zone
drop_zone = tk.Label(root, text="Drop Files Here", relief="solid", width=50, height=10, bg=themes[current_theme]["button_bg"], fg=themes[current_theme]["button_fg"])
drop_zone.pack(pady=20)
drop_zone.drop_target_register(DND_FILES)
drop_zone.dnd_bind('<<Drop>>', on_drop)

# Browse Files Button
browse_button = tk.Button(root, text="Browse Files", command=browse_files, bg=themes[current_theme]["button_bg"], fg=themes[current_theme]["button_fg"])
browse_button.pack(pady=10)

# File List
file_listbox = tk.Listbox(root, width=50, height=10, bg=themes[current_theme]["bg"], fg=themes[current_theme]["fg"])
file_listbox.pack(pady=10)

# Preview Area
preview_label = tk.Label(root, text="Preview will appear here", relief="solid", width=50, height=10, bg=themes[current_theme]["button_bg"], fg=themes[current_theme]["button_fg"])
preview_label.pack(pady=10)

# Folder Organization
folder_frame = tk.Frame(root, bg=themes[current_theme]["bg"])
folder_frame.pack(pady=10)
folder_label = tk.Label(folder_frame, text="Create Folder:", bg=themes[current_theme]["bg"], fg=themes[current_theme]["fg"])
folder_label.pack(side=tk.LEFT)
folder_entry = tk.Entry(folder_frame, width=20)
folder_entry.pack(side=tk.LEFT, padx=5)
create_folder_button = tk.Button(folder_frame, text="Create", command=create_folder, bg=themes[current_theme]["button_bg"], fg=themes[current_theme]["button_fg"])
create_folder_button.pack(side=tk.LEFT)

# Theme Toggle Button
theme_button = tk.Button(root, text="Toggle Theme", command=toggle_theme, bg=themes[current_theme]["button_bg"], fg=themes[current_theme]["button_fg"])
theme_button.pack(pady=10)

# Start Server Button
start_server_button = tk.Button(root, text="Start Sharing", command=lambda: [start_server_thread(), show_qr_code()], bg=themes[current_theme]["button_bg"], fg=themes[current_theme]["button_fg"])
start_server_button.pack(pady=10)

# QR Code Label
qr_label = tk.Label(root, text="QR Code will appear here", relief="solid", width=50, height=5, bg=themes[current_theme]["button_bg"], fg=themes[current_theme]["button_fg"])
qr_label.pack(pady=10)

# Save preferences on exit
root.protocol("WM_DELETE_WINDOW", lambda: [save_preferences(), root.destroy()])

# Run the application
root.mainloop()