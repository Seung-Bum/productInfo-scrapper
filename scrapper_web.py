import math
import re
import urllib3
from util.utilBase64 import encodingBase64
from util.utilSoup import make_soup
urllib3.disable_warnings()  # SSL error 방지


class get_product_info_class_web:
    idx = 0

    def get_product_page(self, param):
        sectid = param['sectid']
        mainUrl = f'https://www.gsshop.com/shop/sect/sectM.gs?sectid={sectid}'
        mainSoup = make_soup(mainUrl)
        category_title = mainSoup.find("h2", "shop-title").get_text()
        prd_total_cnt = mainSoup.find("span", id="prd_cnt_").text  # 전체 상품수 카운트
        prd_total_cnt = int(re.sub(r'[^0-9]', '', prd_total_cnt))

        # 전체 상품수 / 한페이지의 상품 갯수 = 전체 페이지 (전체 페이지를 blind 해놔서 이렇게 구해야함)
        page_cnt = math.ceil(prd_total_cnt / 60)
        print('product_total: ' + str(prd_total_cnt))
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
        return category_title, product_info_list

    def get_product_list(self, url):
        rsltList = []
        soup = make_soup(url)
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

    def get_product_info(self, url):  # 상품 url을 받아서 상품의 타이틀과 상태를 리턴한다. 품절 상품만 리턴
        url = url[0:int(url.find('\''))]
        soup = make_soup(url)
        title = soup.find("p", "product-title").text
        try:
            status = soup.find("span", "gs-btn red color-only gient").text
            print("  .title : " + title)
            print("  .status : " + status)
            if (status == '품절'):
                return {'idx': self.idx, 'title': title, 'status': status, 'link': url}
        except:
            print("  .NoneType Error")  # 버튼의 형태가 바로구매, 품절이 아닌 다른 상태
            # return {'idx': self.idx, 'title': title, 'status': 'OtherStatus', 'link': url}
