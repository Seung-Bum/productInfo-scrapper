import tkinter as tk
import logging
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

        # Set up logging
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

        self.logger = logging.getLogger("LogMonitorApp")

        # Redirect the log output to the Text widget
        self.text_handler = TextHandler(self.log_text)
        self.logger.addHandler(self.text_handler)

    def start_logging(self):
        # Simulate some log messages
        for i in range(5):
            self.logger.info(f"Log message {i}")
            time.sleep(1)


class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.config(state="normal")
        self.text_widget.insert("end", msg + "\n")
        self.text_widget.config(state="disabled")
        self.text_widget.yview(tk.END)  # Auto-scroll to the bottom


if __name__ == "__main__":
    root = tk.Tk()
    app = LogMonitorApp(root)
    app.start_logging()
    root.mainloop()
