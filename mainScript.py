import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from bankers import BankersVisualization  
from visPage import PageReplacementVisualization  

def run_bankers_algorithm_from_ui():
    bankers_window = tk.Toplevel()
    bankers_window.title("Banker's Algorithm Visualization")
    
    messagebox.showinfo("Banker's Algorithm", "Running Banker's Algorithm visualization...")

    bankers_vis = BankersVisualization()

    bankers_vis.update_visualization()

    bankers_window.quit()

def run_fifo_page_replacement_from_ui():
    fifo_window = tk.Toplevel()
    fifo_window.title("FIFO Page Replacement Visualization")
    
    messagebox.showinfo("FIFO Page Replacement", "Running FIFO Page Replacement visualization...")

    fifo_vis = PageReplacementVisualization()

    plt.tight_layout()
    plt.show()

    fifo_window.quit()

def run_algorithms():
    run_bankers_algorithm_from_ui()
    
   
    run_fifo_page_replacement_from_ui()

def exit_program():
    root.quit()

root = tk.Tk()
root.title("Running Algorithms")
root.geometry("400x300")  

label = tk.Label(root, text="Running Algorithms One by One", font=("Arial", 14))
label.pack(pady=50)

button_run_algorithms = tk.Button(root, text="Run Algorithms", command=run_algorithms, font=("Arial", 12), width=30)
button_run_algorithms.pack(pady=10)

button_exit = tk.Button(root, text="Exit", command=exit_program, font=("Arial", 12), width=30)
button_exit.pack(pady=20)

root.mainloop()
