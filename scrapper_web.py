import math
import requests
import re
from bs4 import BeautifulSoup
from utilBase64 import encodingBase64


class get_product_info_class_web:

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
            pageEncoding = str(encodingBase64(page))
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
            return {'idx': self.idx, 'title': title, 'status': status, 'link': url}
        except:
            print("  .NoneType Error")
            return {'idx': self.idx, 'title': title, 'status': 'OtherStatus', 'link': url}
