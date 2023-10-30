import tkinter

window = tkinter.Tk()

window.title("ProductInfo-Scrapper")
window.geometry("240x200+100+100")
window.resizable(True, True)

label = tkinter.Label(window, text="sectid를 입력해주세요.")
label.pack()


def run(event):
    label1.config(text="실행중")
    print(str(entry.get()))


entry = tkinter.Entry(window)
entry.bind("<Return>", run)
entry.pack()

label1 = tkinter.Label(window)
label1.pack()


count = 0


def countUP():
    global count
    count += 1
    label.config(text=str(count))


label = tkinter.Label(window, text="0")
label.pack()

button = tkinter.Button(window, overrelief="solid", width=15, text="such",
                        command=countUP, repeatdelay=1000, repeatinterval=100)
button.pack()

window.mainloop()
