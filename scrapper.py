import base64
import requests
import time
import urllib3
import random
# from fake_useragent import UserAgent
# from random_user_agent.user_agent import UserAgent as random_userAgent
from bs4 import BeautifulSoup
from urllib.request import urlopen


class productInfoExtract:
    urllib3.disable_warnings()

    # 상품 개별 index(get_detail_product에서 증가)
    idx = 0
    headers = {"User-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
               "Accept-Language": 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'}

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
        mainUrl = f"https://www.gsshop.com/shop/sect/sectM.gs?sectid={sectid}&eh=eyJwYWdlTnVtYmVyIjoxLCJzZWxlY3RlZCI6Im9wdC1wYWdlIn0="
        print("  .mainUrl : " + mainUrl)
        # headers = {"User-agent": random.choice(self.UA_DESKTOP)}
        # headers = {"User-agent": self.headers}
        time.sleep(random.uniform(1, 3))
        req = requests.get(mainUrl, headers=self.headers)
        soup = BeautifulSoup(req.text, 'html.parser')

        # a = urlopen(mainUrl)
        # soup = BeautifulSoup(a.read(), 'html.parser')
        title = soup.find('h2', 'shop-title')
        title = title.text.replace("\n", "")
        title = str(title)
        print("  .title : " + title)
        return title

    def get_product_status(self, sectid):
        print("- get_product_status START")
        detailList_result = []
        page = "{\"pageNumber\":var,\"selected\": \"opt-page\"}"

        # sectid를 param로 받음, 상품 카테고리마다 다르다
        subUrl = f"https://www.gsshop.com/shop/sect/sectM.gs?sectid={sectid}&eh="

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

        time.sleep(random.uniform(1, 5))
        # headers = {"User-agent": self.headers}
        req = requests.get(url, headers=self.headers, verify=False)
        soup = BeautifulSoup(req.text, "lxml")

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

            # 상품 상태 추출
            try:
                rsltStatus = self.extract_Status(detailUrl, self.idx)
                print("product_detail : " + str(rsltStatus))
                rsltList.append(rsltStatus)
            except:
                rsltStatus = self.extract_Status(detailUrl, self.idx)
                print("product_detail : " + str(rsltStatus))
                rsltList.append(rsltStatus)

        return rsltList

    # 상품 url을 받아서 상품의 타이틀과 상태를 리턴한다.
    def extract_Status(self, url, idx):
        print("- extract_Status START")

        time.sleep(random.uniform(1, 5))
        # headers = {"User-agent": self.headers}
        req = requests.get(url, headers=self.headers, verify=False)
        soup = BeautifulSoup(req.text, "lxml")

        # a = urlopen(url)
        # soup = BeautifulSoup(a.read(), 'html.parser')

        title = soup.find("p", "product-title").text
        print("  .title : " + title)
        status = soup.find("span", "gs-btn red color-only gient").text
        print("  .status : " + status)
        return {'idx': idx, 'title': title, 'status': status, 'link': url}
