import tkinter as tk
import time

# Function to append a log message to the Text widget


def append_log(message):
    log_text.insert(tk.END, message + "\n")
    log_text.update()
    log_text.see(tk.END)  # Scroll to the end

# Function to simulate generating log messages


def generate_logs():
    for i in range(1, 11):
        log_message = f"Log Message {i}"
        time.sleep(1)
        append_log(log_message)
        root.update_idletasks()
        # root.after(1000)  # Delay between log messages in milliseconds


# Create the main tkinter window
root = tk.Tk()
root.title("Real-Time Log Viewer")

# Create a Text widget for log display
log_text = tk.Text(root, wrap=tk.NONE)
log_text.pack(fill=tk.BOTH, expand=True)

# Create a scrollbar for the Text widget
scrollbar = tk.Scrollbar(log_text)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
log_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=log_text.yview)

# Start a thread or function to generate log messages
generate_logs()

# Run the tkinter main loop
root.mainloop()
