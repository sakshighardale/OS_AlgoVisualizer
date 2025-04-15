import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from bankers import BankersVisualization  # Import Banker's Algorithm visualization class
from visPage import PageReplacementVisualization  # Import FIFO Page Replacement visualization class

# Function to run the Banker's Algorithm visualization
def run_bankers_algorithm_from_ui():
    # Create a new window for Banker's Algorithm visualization
    bankers_window = tk.Toplevel()
    bankers_window.title("Banker's Algorithm Visualization")
    
    # Messagebox showing info
    messagebox.showinfo("Banker's Algorithm", "Running Banker's Algorithm visualization...")

    # Create an instance of the Banker's Algorithm visualization
    bankers_vis = BankersVisualization()

    # Update the visualization after running the algorithm
    bankers_vis.update_visualization()

    # Close the Banker's algorithm window after it's done
    bankers_window.quit()

# Function to run the FIFO Page Replacement visualization
def run_fifo_page_replacement_from_ui():
    # Create a new window for FIFO Page Replacement visualization
    fifo_window = tk.Toplevel()
    fifo_window.title("FIFO Page Replacement Visualization")
    
    # Messagebox showing info
    messagebox.showinfo("FIFO Page Replacement", "Running FIFO Page Replacement visualization...")

    # Create an instance of the FIFO Page Replacement visualization
    fifo_vis = PageReplacementVisualization()

    # Show the FIFO visualization
    plt.tight_layout()
    plt.show()

    # Close the FIFO window after it's done
    fifo_window.quit()

# Function to run both algorithms one after the other
def run_algorithms():
    # First run Banker's Algorithm
    run_bankers_algorithm_from_ui()
    
    # Then run FIFO Page Replacement after Banker's Algorithm completes
    run_fifo_page_replacement_from_ui()

# Function to exit the program
def exit_program():
    root.quit()

# Set up the main window
root = tk.Tk()
root.title("Running Algorithms")
root.geometry("400x300")  # Increased size for better layout

# Add a label
label = tk.Label(root, text="Running Algorithms One by One", font=("Arial", 14))
label.pack(pady=50)

# Create a button to start running both algorithms
button_run_algorithms = tk.Button(root, text="Run Algorithms", command=run_algorithms, font=("Arial", 12), width=30)
button_run_algorithms.pack(pady=10)

# Add exit button
button_exit = tk.Button(root, text="Exit", command=exit_program, font=("Arial", 12), width=30)
button_exit.pack(pady=20)

# Run the main window's event loop
root.mainloop()
