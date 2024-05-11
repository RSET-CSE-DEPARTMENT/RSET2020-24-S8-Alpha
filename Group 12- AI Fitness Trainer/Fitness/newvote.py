#import tempfile
#import time
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.font import Font
import sqlite3
con = sqlite3.connect(database="SecureVoteX.db")
cur = con.cursor()
existing_window = None
def newvote():
    def register():
        name = name_entry.get()
        uid = uid_entry.get()
        v = "voter"
        print("Name:", name)
        print("UID:", uid)
        print("Image Path:", image_path)

    def browse_image():
        global image_path
        image_path = filedialog.askopenfilename(filetypes=[("JPG files", "*.jpg")])
        image_label.config(text="Selected Image: " + image_path)
    global existing_window  # Declare the variable as global to modify it inside the function

    if existing_window and existing_window.winfo_exists():  # Check if the existing window exists and is not closed
        existing_window.destroy()
    window =tk.Toplevel()
    window.title("Voter Registration")
    window.geometry("600x500")  # Set the window size to 600x500 pixels
    window.configure(bg="#2b2b2b")  # Set background color

    # Custom font
    heading_font = Font(family="Helvetica", size=20, weight="bold")
    label_font = Font(family="Helvetica", size=12, weight="bold")
    button_font = Font(family="Helvetica", size=12)

    # Frame for "New Registration" label
    frame = tk.Frame(window, bg="#242424")
    frame.pack(fill="x", pady=10)

    # Heading label
    heading_label = tk.Label(frame, text="Voter Registration", font=heading_font, fg="#FFFFFF", bg="#242424")
    heading_label.pack(pady=10)

    # Name label and entry
    name_label = tk.Label(window, text="Enter Name:", font=label_font, fg="white", bg="#2b2b2b")
    name_label.pack(pady=5)

    name_entry = tk.Entry(window, font=label_font, bg="#353638", fg="white")
    name_entry.pack(pady=5)

    # UID label and entry
    uid_label = tk.Label(window, text="Enter UID:", font=label_font, fg="white",bg="#2b2b2b")
    uid_label.pack(pady=5)

    uid_entry = tk.Entry(window, font=label_font, bg="#353638", fg="white")
    uid_entry.pack(pady=5)

    # Upload label
    upload_label = tk.Label(window, text="Upload Picture", font=label_font, fg="white",bg="#2b2b2b")
    upload_label.pack(pady=5)

    # Browse button
    browse_button = tk.Button(window, text="Browse", command=browse_image, font=button_font, bg="#1f69a6", fg="white")
    browse_button.pack(pady=5)

    # Selected image label
    image_label = tk.Label(window, text="Selected Image:", font=label_font, fg="white",bg="#2b2b2b")
    image_label.pack(pady=5)

    # Register button
    register_button = tk.Button(window, text="Register", command=register, font=button_font, bg="#1f69a6", fg="white")
    register_button.pack(pady=10)

    # Center the window content
    window.update_idletasks()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    window.geometry(f"+{x}+{y}")
    window.protocol("WM_DELETE_WINDOW", on_close)

    existing_window = window  # Update the reference to the existing window

    window.mainloop()
def on_close():
    global existing_window  # Declare the variable as global to modify it inside the function
    if existing_window:
        existing_window.destroy()  # Destroy the existing window
    existing_window = None  # Reset the reference to the existing window

#newvote()