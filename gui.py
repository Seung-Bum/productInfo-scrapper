import time
import tkinter
from flask import redirect, render_template, request
from scrapper import productInfoExtract


def productAllExtract(param):
    print("- productAllExtract START ---------------------------------")
    start = time.time()
    sectid = param
    # sectid = request.args.get('sectid')
    product_info_extract = productInfoExtract()
    if sectid:
        print("  .sectid : " + str(sectid))
        title = product_info_extract.get_title(sectid)
        detailList = product_info_extract.get_product_status(sectid)
    else:
        print("  .sectid : NONE")
        return redirect("/")
    end = time.time()
    print("- productAllExtract end ---------------------------------")
    print(f"{end - start:.2f} sec")

    # 엑셀로 데이터를 저장하는 메서드 필요
    return  # render_template("report.html", title=title, rslt_list=detailList)


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
    productAllExtract(sectid)
    label1.config(text="완료")


entry = tkinter.Entry(window)
entry.bind("<Return>", run)
entry.pack()

label1 = tkinter.Label(window)
label1.pack()

window.mainloop()
