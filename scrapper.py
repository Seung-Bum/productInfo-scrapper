import base64
import requests
import time
import urllib3
import random
from fake_useragent import UserAgent
from random_user_agent.user_agent import UserAgent as random_userAgent
from bs4 import BeautifulSoup
from urllib.request import urlopen


class productInfoExtract:
    urllib3.disable_warnings()

    # 상품 개별 index(get_detail_product에서 증가)
    idx = 0
    UA_DESKTOP = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
        "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/99.0.1150.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
    ]

    def __init__(self):
        self.str = ""
        self.param_list = ""
        self.url = ""
        self.index = ""

    def encodingBase64(self, str):
        bytes = str.encode('UTF-8')
        result = base64.b64encode(bytes)
        # result_str = result.decode('ascii')
        print("  .base64 encoding success")
        return result

    def get_title(self, sectid):
        mainUrl = f"http://www.gsshop.com/shop/sect/sectM.gs?sectid={sectid}&eh=eyJwYWdlTnVtYmVyIjoxLCJzZWxlY3RlZCI6Im9wdC1wYWdlIn0="
        print("  .mainUrl : " + mainUrl)
        # ua = UserAgent()
        headers = {"User-agent": random.choice(self.UA_DESKTOP)}
        req = requests.get(mainUrl, headers=headers, verify=False)
        soup = BeautifulSoup(req.text, "lxml")  # html에 대하여 접근할 수 있도록

        # req = requests.get(mainUrl)
        # soup = BeautifulSoup(req.text, "html.parser")

        # a = urlopen(mainUrl)
        # soup = BeautifulSoup(a.read(), 'html.parser')
        title = soup.find('h2', 'shop-title')
        title = title.text.replace("\n", "")
        print("  .title : " + title)
        return title

    def get_product_status(self, sectid):
        print("- get_product_status START")
        detailList_result = []
        page = "{\"pageNumber\":var,\"selected\": \"opt-page\"}"

        # sectid를 param로 받음, 상품 카테고리마다 다르다
        subUrl = f"http://www.gsshop.com/shop/sect/sectM.gs?sectid={sectid}&eh="

        # 전체 페이지 loop(최대 100페이지 까지만 parsing)
        for i in range(1, 101):
            page = page.replace('var', str(i))
            pageEncoding = self.encodingBase64(page)
            pageEncoding = str(pageEncoding)
            print("  .page : " + page)
            print("  .encoding : " + pageEncoding)
            subUrl = subUrl + pageEncoding[2:-2]
            print("  .subUrl : " + subUrl)

            # url이 700자가 넘어갈 경우 없는 페이지로 판단
            subUrl_len = len(subUrl)
            if (subUrl_len > 700):
                print("  .END PAGE")
                return detailList_result

            # 상품 진열 페이지
            detailList_result += self.get_detail_product(subUrl)

            # for문이 끝날때 다시 숫자를 var로 변경함
            page = page.replace(str(i), 'var')
        return detailList_result

    # 상품 진열 페이지
    def get_detail_product(self, url):
        print("- get_detail_status STRAT")
        rsltList = []
        # ua = UserAgent()
        headers = {"User-agent": random.choice(self.UA_DESKTOP)}
        req = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(req.text, "lxml")  # html에 대하여 접근할 수 있도록

        # req = requests.get(url, verify=False)
        # soup = BeautifulSoup(req.text, "html.parser")

        # a = urlopen(url)
        # soup = BeautifulSoup(a.read(), 'html.parser')

        buttonTags = soup.find_all('button', 'link-new-tab')
        buttonTags_len = len(buttonTags)
        print('  .buttonTags len : ' + str(buttonTags_len))

        for i in buttonTags:
            self.idx += 1
            orginStr = str(i)
            index1 = int(str(orginStr.find("https")))
            index2 = int(str(orginStr.find("§id")))
            detailUrl = orginStr[index1:index2]
            detailUrl = detailUrl.replace('https', 'http')

            time.sleep(1.5)
            # 상품 상태 추출
            rsltStatus = self.extract_Status(detailUrl, self.idx)
            print("product_detail : " + str(rsltStatus))
            rsltList.append(rsltStatus)
        return rsltList

    # 상품 url을 받아서 상품의 타이틀과 상태를 리턴한다.
    def extract_Status(self, url, idx):
        print("- extract_Status START")
        # ua = UserAgent()
        headers = {"User-agent": random.choice(self.UA_DESKTOP)}
        req = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(req.text, "lxml")  # html에 대하여 접근할 수 있도록

        # req = requests.get(url, verify=False)
        # soup = BeautifulSoup(req.text, "html.parser")

        # a = urlopen(url)
        # soup = BeautifulSoup(a.read(), 'html.parser')

        title = soup.find("p", "product-title").text
        print("  .title : " + title)
        status = soup.find("span", "gs-btn red color-only gient").text
        print("  .status : " + status)
        return {'idx': idx, 'title': title, 'status': status, 'link': url}
