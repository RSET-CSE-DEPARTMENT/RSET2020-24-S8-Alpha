import tkinter as tk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def generate_chart(electrodes, label, stressed, relaxed):
    # Electrode mapping dictionary
    electrode_mapping = {
        1: "EEG Fp1",
        2: "EEG Fp2",
        3: "EEG F3",
        4: "EEG F4",
        5: "EEG F7",
        6: "EEG F8",
        7: "EEG T3",
        8: "EEG T4",
        9: "EEG C3",
        10: "EEG C4",
        11: "EEG T5",
        12: "EEG T6",
        13: "EEG P3",
        14: "EEG P4",
        15: "EEG O1",
        16: "EEG O2",
        17: "EEG Fz",
        18: "EEG Cz",
        19: "EEG Pz",
        20: "EEG A2-A1"
    }

    # Create a new window for the chart
    chart_window = tk.Toplevel()
    chart_window.title(f"Charts for {label}")

    # Set the size of the window
    chart_window.geometry("800x600")

    # Create a figure for the chart
    fig = Figure(figsize=(8, 6), dpi=100)

    for i, electrode in enumerate(electrodes):
        # Create a subplot for each electrode
        ax = fig.add_subplot(3, 1, i+1)

        # Extract values for the current label and electrode from both stressed and relaxed dataframes
        stressed_values = stressed.iloc[:, electrode]
        relaxed_values = relaxed.iloc[:, electrode]

        # Plot stressed state data in red
        ax.plot(stressed_values, 'r', label='Stressed State')

        # Plot relaxed state data in blue
        ax.plot(relaxed_values, 'b', label='Relaxed State')

        # Set plot title and labels
        ax.set_title(f'{label} for {electrode_mapping[electrode]}')  # Use electrode mapping dictionary to get electrode name
        ax.set_xlabel('Subjects')
        ax.set_ylabel(label)

        # Add legend
        ax.legend()

    # Adjust spacing between subplots
    fig.subplots_adjust(hspace=0.5)

    # Add the figure to the chart window
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Function to open the view results window
def open_view_results_window():
    # Create the view results window
    view_results_window = tk.Toplevel()
    view_results_window.title("View Results")

    # Set the initial size of the window
    view_results_window.geometry("800x600")

    # Add title for Available Results
    title_label = tk.Label(view_results_window, text="Available Results", font=("Arial", 14, "bold"))
    title_label.pack()

    # Read the data from CSV files
    stressed_hfd_df = pd.read_csv("Features/stressed_hfd_values.csv")
    relaxed_hfd_df = pd.read_csv("Features/relaxed_hfd_values.csv")
    stressed_rtp_df = pd.read_csv("Features/stressed_theta_power.csv")
    relaxed_rtp_df = pd.read_csv("Features/relaxed_theta_power.csv")
    stressed_rap_df = pd.read_csv("Features/stressed_alpha_power.csv")
    relaxed_rap_df = pd.read_csv("Features/relaxed_alpha_power.csv")

    # Define electrodes for different features
    hfd_electrodes = [1, 3, 6]
    rel_theta_electrodes = [17, 1, 2]
    rel_alpha_electrodes = [15, 13, 19]

    # Create buttons for each feature
    button1 = tk.Button(view_results_window, text="Higuchi Fractal Dimension", command=lambda: generate_chart(hfd_electrodes, "Higuchi Fractal Dimension", stressed_hfd_df, relaxed_hfd_df), padx=20, pady=10)
    button1.pack(pady=10)

    button2 = tk.Button(view_results_window, text="Relative Theta Power", command=lambda: generate_chart(rel_theta_electrodes, "Relative Theta Power", stressed_rtp_df, relaxed_rtp_df), padx=20, pady=10)
    button2.pack(pady=10)

    button3 = tk.Button(view_results_window, text="Relative Alpha Power", command=lambda: generate_chart(rel_alpha_electrodes, "Relative Alpha Power", stressed_rap_df, relaxed_rap_df), padx=20, pady=10)
    button3.pack(pady=10)

    # Start the Tkinter event loop for the view results window
    view_results_window.mainloop()
