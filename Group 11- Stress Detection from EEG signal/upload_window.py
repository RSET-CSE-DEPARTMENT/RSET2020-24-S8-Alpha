import tkinter as tk
from tkinter import filedialog
import subprocess
import threading
import view_results

def open_upload_window(user_type):
    # Create the main application window
    app = tk.Tk()
    app.title("File Upload GUI")
    
    # Set the initial size of the window
    app.geometry("1920x1080")

    # Create a Canvas widget
    canvas = tk.Canvas(app)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a scrollbar to the canvas
    scrollbar = tk.Scrollbar(app, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the canvas to use the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame to contain the widgets
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_configure)

    def upload_files():
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            label.config(text="Files uploaded:\n" + "\n".join(file_paths))
            build_model_button.config(state="normal")  # Enable the build model button
            # Store the file paths for processing when building the model
            app.uploaded_files = file_paths
        else:
            label.config(text="No files selected.")
            build_model_button.config(state="disabled")  # Disable the build model button if no files are selected

    def build_model():
        # Update status label to indicate calculation is in progress
        status_label.config(text="Model building initiated. Please wait...")
        
        # Define a function to run subprocesses asynchronously
        def run_subprocesses():
            processes = []
            for py_file in ['hfd_relaxed.py', 'hfd_stressed.py','psd_calc.py','relative_theta.py','relative_alpha.py']:
                processes.append(subprocess.Popen(['python', py_file] + list(app.uploaded_files)))
            
            # Wait for all subprocesses to finish
            for process in processes:
                process.wait()
            
            # Update status label after all subprocesses finish
            status_label.config(text="Model building finished!")  # Update status label
            view_results_button.config(state="normal")  # Enable the view results button
        
        # Create a thread to run the subprocesses
        threading.Thread(target=run_subprocesses).start()
    
    def view_results():
        import view_results  # Import the module where open_view_results_window() is defined
        view_results.open_view_results_window()

        
    # Create a button to upload files
    upload_button = tk.Button(frame, text="Upload Files", command=upload_files, width=20, height=2)
    upload_button.pack(pady=10)

    # Create a label to display file paths
    label = tk.Label(frame, text="")
    label.pack()

    # Create a button to build the model (initially disabled)
    build_model_button = tk.Button(frame, text="Build Model", command=build_model, width=20, height=2, state="disabled")
    build_model_button.pack(pady=10)
    
    # Create a button to view results (initially disabled)
    view_results_button = tk.Button(frame, text="View Results", command=view_results, width=20, height=2, state="normal")
    view_results_button.pack(pady=10)
    
    # Create a label to show status
    status_label = tk.Label(frame, text="")
    status_label.pack()

    # Start the Tkinter event loop
    app.mainloop()

