import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import GPUtil
import psutil

# Create a function to get CPU usage percentage
def get_cpu_usage():
    try:
        # Get the current CPU usage percentage using psutil
        return psutil.cpu_percent(interval=1)
    except Exception:
        return 0.0

# Create a function to get GPU usage percentage
def get_gpu_usage():
    try:
        # Get the current GPU usage percentage
        gpu = GPUtil.getGPUs()[0]
        return gpu.load * 100
    except Exception:
        return 0.0

# Create a function to get RAM usage percentage
def get_ram_usage():
    try:
        # Get the current RAM usage percentage using psutil
        return psutil.virtual_memory().percent
    except Exception:
        return 0.0

# Create the main window
window = tk.Tk()
window.title("System Metrics Monitor")

# Modify the update_graphs() function
def update_graphs():
    cpu_percent = get_cpu_usage()
    gpu_percent = get_gpu_usage()
    ram_percent = get_ram_usage()

    # Update CPU usage data
    if len(cpu_usage_data) >= 50:
        cpu_usage_data.pop(0)
    cpu_usage_data.append(cpu_percent)

    # Update GPU usage data
    if len(gpu_usage_data) >= 50:
        gpu_usage_data.pop(0)
    gpu_usage_data.append(gpu_percent)

    # Update RAM usage data
    if len(ram_usage_data) >= 50:
        ram_usage_data.pop(0)
    ram_usage_data.append(ram_percent)

    # Create a list of x values for the graph with negative time offset
    x_values = list(range(-50, 0))  # 50 data points, starting from -50 to -1

    # Clear the combined plot and replot all metrics
    combined_ax.clear()
    cpu_line, = combined_ax.plot(x_values, cpu_usage_data, label='CPU', color='blue')
    gpu_line, = combined_ax.plot(x_values, gpu_usage_data, label='GPU', color='green')
    ram_line, = combined_ax.plot(x_values, ram_usage_data, label='RAM', color='red')
    combined_ax.set_ylim(0, 100)
    combined_ax.set_title("System Usage (%)")
    combined_ax.set_xlabel("Time Offset (seconds)")
    combined_ax.set_ylabel("Usage (%)")

    # Add grids to both x and y axes
    combined_ax.grid(True)
    combined_ax.set_xticks(range(-50, 1, 5))

    # Set the y-axis ticks by 10s
    combined_ax.set_yticks(range(0, 101, 5))

    # Make the lines at -20, -40, -60, and -80 bold
    combined_ax.axhline(10, color='gray', linestyle='--')
    combined_ax.axhline(20, color='gray', linestyle='--')
    combined_ax.axhline(30, color='gray', linestyle='--')
    combined_ax.axhline(40, color='gray', linestyle='--')
    combined_ax.axhline(50, color='gray', linestyle='--')
    combined_ax.axhline(60, color='gray', linestyle='--')
    combined_ax.axhline(70, color='gray', linestyle='--')
    combined_ax.axhline(80, color='gray', linestyle='--')
    combined_ax.axhline(90, color='gray', linestyle='--')

    # Set the legend
    combined_ax.legend(loc='upper right')

    # Add the latest percentage labels on top of the lines with matching colors
    combined_ax.text(x_values[-1], cpu_usage_data[-1], f'{cpu_usage_data[-1]:.1f}%', ha='center', va='bottom', color='blue', fontsize=8)
    combined_ax.text(x_values[-1], gpu_usage_data[-1], f'{gpu_usage_data[-1]:.1f}%', ha='center', va='bottom', color='green', fontsize=8)
    combined_ax.text(x_values[-1], ram_usage_data[-1], f'{ram_usage_data[-1]:.1f}%', ha='center', va='bottom', color='red', fontsize=8)

    combined_canvas.draw()

    window.after(1000, update_graphs)  # Update every 1 second

# Set the window size to be moderately medium
window.geometry("600x450")  # Width x Height

# Create a single-column grid layout with a weight for the row
frame_left = tk.Frame(window)
frame_left.grid(row=0, padx=10, pady=10, sticky="nsew")

# Configure row and column proportions
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Create a combined usage graph
combined_fig, combined_ax = plt.subplots(figsize=(6, 4))
combined_ax.set_ylim(0, 100)
combined_ax.set_title("System Usage (%)")

# Initialize data lists
cpu_usage_data = [0] * 50
gpu_usage_data = [0] * 50
ram_usage_data = [0] * 50

# Create a FigureCanvasTkAgg for the combined graph
combined_canvas = FigureCanvasTkAgg(combined_fig, master=frame_left)
combined_canvas_widget = combined_canvas.get_tk_widget()
combined_canvas_widget.grid(row=0, sticky="nsew")

# Start updating the graphs
update_graphs()

# Start the main event loop
window.mainloop()
