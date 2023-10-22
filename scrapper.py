import base64
from bs4 import BeautifulSoup
from urllib.request import urlopen


class productInfoExtract:

    # 상품 개별 index(get_detail_product에서 증가)
    idx = 0

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

    # 메인 url
    def get_product_status(self, param_list):
        print("- get_product_status START")
        detailList_result = []

        # 나중에 sectid를 param으로 받아야 할듯함 상품마다 다르다
        mainUrl = f"https://www.gsshop.com/shop/sect/sectM.gs?sectid={param_list[0]}&lsectid={param_list[1]}&msectid={param_list[2]}&lseq={param_list[3]}&gsid={param_list[4]}"
        subUrl = "https://www.gsshop.com/shop/sect/sectM.gs?sectid=1661646&eh="
        print("  .mainUrl : " + mainUrl)

        a = urlopen(mainUrl)
        soup = BeautifulSoup(a.read(), 'html.parser')
        title = soup.find('h2', 'shop-title')
        title = title.text.replace("\n", "")
        print("  .title : " + title)

        page = "{\"pageNumber\":var,\"selected\": \"opt-page\"}"
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

            # 디테일 페이지 extract (type check 후 리스트 중첩)
            detailList = self.get_detail_product(subUrl)
            detailList_result += detailList

            # for문이 끝날때 다시 숫자를 var로 변경함
            page = page.replace(str(i), 'var')
        return detailList_result

    # 상품의 세부 정보 페이지
    def get_detail_product(self, url):
        print("- get_detail_status STRAT")
        rsltList = []
        a = urlopen(url)
        soup = BeautifulSoup(a.read(), 'html.parser')
        buttonTags = soup.find_all('button', 'link-new-tab')
        buttonTags_len = len(buttonTags)
        print('  .buttonTags len : ' + str(buttonTags_len))

        for i in buttonTags:
            self.idx += 1
            orginStr = str(i)
            index1 = int(str(orginStr.find("https")))
            index2 = int(str(orginStr.find("§id")))
            detailUrl = orginStr[index1:index2]

            # 상품 개별 상태 추출
            rsltStatus = self.extract_Status(detailUrl, self.idx)
            print(rsltStatus)
            rsltList.append(rsltStatus)
        return rsltList

    # 상품 url을 받아서 상품의 타이틀과 상태를 리턴한다.
    def extract_Status(self, url, idx):
        print("- extract_Status START")
        a = urlopen(url)
        soup = BeautifulSoup(a.read(), 'html.parser')
        title = soup.find("p", "product-title").text
        print("  .title : " + title)
        status = soup.find("span", "gs-btn red color-only gient").text
        print("  .status : " + status)
        return {
            'idx': idx,
            'title': title,
            'status': status,
            'link': url
        }
