import tkinter as tk
from scrapper import productInfoExtract


def run(event):
    sectid = entry.get()
    print("setid : " + str(sectid))
    productInfoExtract().productAllExtract(sectid)
    label1.config(text="완료")


# Function to append a log message to the Text widget
def append_log(message):
    log_text.insert(tk.END, message + "\n")
    log_text.update()
    log_text.see(tk.END)  # Scroll to the end


# Function to simulate generating log messages
# def generate_logs():
#     for i in range(1, 11):
#         log_message = f"Log Message {i}"
#         append_log(log_message)
#         window.update_idletasks()
    # root.after(1000)  # Delay between log messages in milliseconds


# Create the main tkinter window
window = tk.Tk()
window.title("ProductInfo-Scrapper")
window.geometry('800x760')
window.resizable(True, True)

# Create a Text widget for log display
log_text = tk.Text(window, wrap=tk.NONE)
log_text.pack(fill=tk.BOTH, expand=True)

# Create a scrollbar for the Text widget
scrollbar = tk.Scrollbar(log_text)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
log_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=log_text.yview)

label = tk.Label(window, text="sectid를 입력해주세요.")
label.pack()

entry = tk.Entry(window)
entry.bind("<Return>", run)
entry.pack()

label1 = tk.Label(window)
label1.pack()

window.mainloop()
