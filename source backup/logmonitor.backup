import tkinter as tk
import time


class LogMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Log Monitor")

        self.log_text = tk.Text(root, wrap="none", state="disabled")
        self.log_text.pack(expand=True, fill="both")

        self.scrollbar = tk.Scrollbar(self.root, command=self.log_text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=self.scrollbar.set)

        self.file_path = "./logfile.log"
        self.update_log()

    def update_log(self):
        with open(self.file_path, "r") as log_file:
            log_content = log_file.read()

        self.log_text.config(state="normal")
        self.log_text.delete(1.0, "end")
        self.log_text.insert("end", log_content)
        self.log_text.config(state="disabled")

        # Update every 1000 milliseconds (1 second)
        self.root.after(1000, self.update_log)


if __name__ == "__main__":
    root = tk.Tk()
    app = LogMonitorApp(root)
    root.mainloop()
