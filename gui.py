import tkinter
from scrapper import productInfoExtract

window = tkinter.Tk()

window.title("ProductInfo-Scrapper")
window.geometry("240x100+100+100")
window.resizable(True, True)

label = tkinter.Label(window, text="sectid를 입력해주세요.")
label.pack()


def run(event):
    label1.config(text="실행중...")
    sectid = entry.get()
    print("setid : " + str(sectid))
    productInfoExtract().productAllExtract(sectid)
    label1.config(text="완료")


entry = tkinter.Entry(window)
entry.bind("<Return>", run)
entry.pack()

label1 = tkinter.Label(window)
label1.pack()

window.mainloop()
