import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess

def browse_photo():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
    if file_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path)

        # Display the browsed image
        display_image(file_path)
    else:
        # Display a message if no image is selected
        image_label.config(text="No Image Input")
        image_label.image = None

def display_image(file_path):
    image = Image.open(file_path)
    image.thumbnail((300, 300))
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo

def run_program():
    file_path = entry_path.get()
    if file_path:
        try:
            # Open the image and convert it to JPG
            image = Image.open(file_path)
            image = image.convert("RGB")

            # Save the converted image as pic.jpg
            save_path = "pic.jpg"
            image.save(save_path)

            # Run another Python program (replace "your_program.py" with the actual program)
            program_path = "testmodel.py"
            command = ["python", program_path, save_path]
            process_output = subprocess.check_output(command, universal_newlines=True)

            # Display the text output in the same GUI window
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, process_output)

            # Update the labels with file paths
            path_label.config(text=f"Path: {file_path}")
            image_label.config(text=f"Image: {save_path}")
            output_label.config(text="Output:")

        except Exception as e:
            # Handle any exceptions that may occur during image processing or program execution
            print(f"Error: {e}")
    else:
        # Display a message if no image is selected
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "No Image Input")

# Create the main application window
root = tk.Tk()
root.title("Dog Breed Identifier")
root.geometry("800x650")  # Set the window size

# Labels and Entry widgets for displaying file paths
path_label = tk.Label(root, text="Path:")
path_label.pack(pady=5)

entry_path = tk.Entry(root, width=40)
entry_path.pack(pady=5)

# Button to browse for a photo
browse_button = tk.Button(root, text="Browse Photo", command=browse_photo)
browse_button.pack(pady=10)

# Add padding between image label and buttons
image_label = tk.Label(root, text="")
image_label.pack(pady=20)

# Button to run the program
run_button = tk.Button(root, text="Run Program", command=run_program)
run_button.pack(pady=10)

# Add padding between output label and text widget
output_label = tk.Label(root, text="Output:")
output_label.pack(pady=5)

output_text = tk.Text(root, height=5, width=60)
output_text.pack(pady=10)

# Start the main event loop
root.mainloop()
