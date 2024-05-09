import tkinter as tk
from tkinter import messagebox
from upload_window import open_upload_window

def open_selection_window():
    # Create the main application window
    app = tk.Tk()
    app.title("User Selection Window")
    
    # Set the initial size of the window (increased from 400x300 to 600x400)
    app.geometry("600x400")

    # Add label for "Stress Detection System" with larger font
    title_label = tk.Label(app, text="Stress Detection System", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    def open_upload_window_with_user(user_type):
        app.destroy()  # Close the user selection window
        open_upload_window(user_type)

    # Create buttons for user selection with larger font
    patient_button = tk.Button(app, text="Patient (Not Implemented)", state="disabled", font=("Arial", 12))
    patient_button.pack(pady=10)
    academician_button = tk.Button(app, text="Academician", command=lambda: open_upload_window_with_user("Academician"), font=("Arial", 12))
    academician_button.pack(pady=10)

    # Start the Tkinter event loop
    app.mainloop()
