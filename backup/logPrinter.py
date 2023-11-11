from tkinter import *
import datetime
import time


class LogPrinter:
    def __init__(self):
        self.tkhandler = Tk()
        self.tkhandler.geometry('800x760')
        self.tkhandler.title('Product_Info_Extract')

        self.label_title = Label(self.tkhandler, text='')
        self.label_title.grid(row=0, column=0, sticky="w")

        # 텍스트 박스에 스크롤 연결
        self.scroll = Scrollbar(self.tkhandler, orient='vertical')
        self.lbox = Listbox(
            self.tkhandler, yscrollcommand=self.scroll.set, width=116, height=500
        )
        self.scroll.config(command=self.lbox.yview)
        self.lbox.grid(row=5, column=10, columnspan=50, sticky="s")

        # 프로그램 시작 안내
        self.append_log('프로그램을 시작했습니다.')

    def append_log(self, msg):
        global now
        self.now = str(datetime.datetime.now())[0:-7]
        self.lbox.insert(END, "[{}] {}".format(self.now, msg))
        self.lbox.update()
        self.lbox.see(END)

    def run(self):
        self.tkhandler.mainloop()


# lp = LogPrinter()
# lp.run()
