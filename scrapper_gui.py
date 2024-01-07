import math
import re
import utilBase64
import requests
import tkinter as tk
from utilExcel import makeExcel
from bs4 import BeautifulSoup
from utilMail import sendEmail


# 데이터 추출이 완료되고, 엑셀이 만들어진 뒤에 이메일이 발송된다.
# 0. run (rungui tkinter에서 실행)
# 1. productAllExtract
#   - makeExcel
#   - sendmail
# 2-1. get_title(sectid)
# 2-2. get_product_status(sectid)
#       - get_detail_product(requetUrl)
#           - extract_Status(detailUrl, self.idx)
#           - append_log(rsltStatus)


class get_product_info_class_gui:

    idx = 0
    headers = {
        "User-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        "Accept-Language": 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        "Accept-Encoding": 'gzip, deflate, br',
        "Cache-Control": 'no-cache',
        "Sec-Fetch-Site": 'same-site',
        "Sec-Fetch-Mode": 'no-cors',
        "Sec-Fetch-Dest": 'script',
    }

    def get_product_page(self, param):
        sectid = param['sectid']
        mainUrl = f'https://www.gsshop.com/shop/sect/sectM.gs?sectid={sectid}'
        mainReq = requests.get(mainUrl, headers=self.headers, verify=False)
        mainSoup = BeautifulSoup(mainReq.text, "lxml")
        category_title = mainSoup.find("h2", "shop-title").get_text()
        prd_total_cnt = mainSoup.find("span", id="prd_cnt_").text
        prd_total_cnt = int(re.sub(r'[^0-9]', '', prd_total_cnt))
        page_cnt = math.ceil(prd_total_cnt / 60)
        print('prd_total_cnt: ' + str(prd_total_cnt))
        print('page_cnt: ' + str(page_cnt))

        product_info_list = []
        for i in range(1, page_cnt+1):
            page = "{\"pageNumber\":var,\"selected\":\"opt-page\"}"
            subUrl = f"https://www.gsshop.com/shop/sect/sectM.gs?sectid={sectid}&eh="
            page = page.replace('var', str(i))
            pageEncoding = str(utilBase64.encodingBase64(page))
            requetUrl = subUrl + pageEncoding[2:-2]
            print("  .page : " + page)
            print("  .requetUrl : " + requetUrl)

            # 상세 진열 페이지의 데이터를 모두 담는다 (page1List[a, b] + page2List[c, d] = resultList[a, b, c, d])
            product_info_list += self.get_product_list(requetUrl)

            # for문이 끝날때 다시 숫자를 var로 변경함
            page = page.replace(str(i), 'var')
        return product_info_list, category_title

    def get_product_list(self, url):
        rsltList = []
        req = requests.get(url, headers=self.headers, verify=False)
        soup = BeautifulSoup(req.text, "lxml")
        buttonTags = soup.find_all('button', 'link-new-tab')
        buttonTags_len = len(buttonTags)
        print('  .buttonTags len : ' + str(buttonTags_len))

        for tag in buttonTags:  # 상품진열 페이지의 버튼들에서 각각의 상품 링크를 가져옴
            self.idx += 1
            orginStr = str(tag)
            index1 = int(str(orginStr.find("https")))
            index2 = int(str(orginStr.find("§id")))
            productUrl = orginStr[index1:index2]
            productUrl = productUrl.replace('https', 'http')

            # 로봇 배제 표준 사항 적용 (해당 상품id면 -1이 아닌 수가 나오게 된다. 해당 상품 Pass)
            if (-1 != productUrl.find('prdid=18549103') or
                -1 != productUrl.find('prdid=19113221') or
                    -1 != productUrl.find('prdid=19856141')):
                print("로봇 배제 표준 사항 적용")
                continue

            # 각각의 상품 상태 추출
            product_info = self.get_product_info(productUrl)
            rsltList.append(product_info)
        return rsltList

    def get_product_info(self, url):  # 상품 url을 받아서 상품의 타이틀과 상태를 리턴한다.
        req = requests.get(url, headers=self.headers, verify=False)
        soup = BeautifulSoup(req.text, "lxml")
        url = url[0:int(url.find('\''))]
        title = soup.find("p", "product-title").text
        try:
            status = soup.find("span", "gs-btn red color-only gient").text
            print("  .title : " + title)
            print("  .status : " + status)
            append_log(
                f"idx: {self.idx}, title: {title}, status: {status}, link: {url}")
            return {'idx': self.idx, 'title': title, 'status': status, 'link': url}
        except:
            print("  .NoneType Error")
            append_log(
                f"idx: {self.idx}, title: {title}, status: OtherStatus, link: {url}")
            return {'idx': self.idx, 'title': title, 'status': 'OtherStatus', 'link': url}

# ==================================================================================
# tkinter gui
# ==================================================================================


def run(event):
    param = {}
    sectid = entry.get()
    to_mail = entry1.get()
    token = entry2.get()
    param['sectid'] = sectid
    param['to_mail'] = to_mail
    param['token'] = token
    print("setid : " + str(sectid))
    print("to_mail : " + str(to_mail))
    product_info_list, category_title = get_product_info_class_gui().get_product_page(param)
    makeExcel(category_title, product_info_list)
    sendEmail(to_mail, token)
    label1.config(text="완료")


def append_log(message):
    # Function to append a log message to the Text widget
    # log_text.insert(tk.END, message + "\n")
    log_text.insert(tk.END, message)
    log_text.insert(tk.END, "\n")
    log_text.update()
    log_text.see(tk.END)  # Scroll to the end


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

label0 = tk.Label(window)  # 공백
label0.pack()

# sectid
label = tk.Label(window, text="sectid를 입력해주세요.")
label.pack()

entry = tk.Entry(window)
entry.bind("<Return>", run)
entry.pack()

# 빈공간
label1 = tk.Label(window)
label1.pack()

# Email
labe2 = tk.Label(window, text="데이터 받을 메일을 입력해주세요. ( ex) test@mail.com )")
labe2.pack()

entry1 = tk.Entry(window)
entry1.bind("<Return>", run)
entry1.pack()

# 빈공간
label3 = tk.Label(window)
label3.pack()

# send_token
labe4 = tk.Label(window, text="mail 인증 Token을 입력해주세요.")
labe4.pack()

entry2 = tk.Entry(window)
entry2.bind("<Return>", run)
entry2.pack()

# 빈공간
label5 = tk.Label(window)
label5.pack()

window.mainloop()
