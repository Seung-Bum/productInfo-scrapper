import math
import re
import urllib3
from flask import Flask, render_template, request
from util.utilSoup import make_soup
urllib3.disable_warnings()  # SSL error 방지

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/productExtract")
def productExtract():
    print("productExtract 시작")
    # 사용자가  입력값 (파라미터)
    mainUrl = request.args.get('mainUrl')
    sectid = request.args.get('sectid')
    email = request.args.get('email')

    mainSoup = make_soup(mainUrl)
    category_title = mainSoup.find("h2", "shop-title").get_text()
    prd_total_cnt = mainSoup.find("span", id="prd_cnt_").text  # 전체 상품수 카운트 찾기
    prd_total_cnt = int(re.sub(r'[^0-9]', '', prd_total_cnt))

    # 전체 상품수 / 한페이지의 상품 갯수 = 전체 페이지 (전체 페이지를 blind 해놔서 이렇게 구해야함)
    page_cnt = math.ceil(prd_total_cnt / 60)
    # print('product_total: ' + str(prd_total_cnt))
    # print('page_cnt: ' + str(page_cnt))

    print("productExtract 종료")
    return {'category_title': category_title, 'prd_total_cnt': prd_total_cnt, 'page_cnt': page_cnt, 'sectid': sectid, 'email': email}


@app.route("/getProductList")
def get_product_list():
    requetUrl = request.args.get('requetUrl')

    rsltList = []
    soup = make_soup(requetUrl)
    buttonTags = soup.find_all('button', 'link-new-tab')
    buttonTags_len = len(buttonTags)
    # print('  .buttonTags len : ' + str(buttonTags_len))

    for tag in buttonTags:  # 상품진열 페이지의 버튼들에서 각각의 상품 링크를 가져옴
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

        # print('   .productUrl : ' + productUrl)
        rsltList.append(productUrl)
    return rsltList


@app.route("/getProductStatus")
def get_product_info():  # 상품 url을 받아서 상품의 타이틀과 상태를 리턴한다. 품절 상품만 리턴

    url = request.args.get('requetUrl')

    url = url[0:int(url.find('\''))]
    soup = make_soup(url)
    title = soup.find("p", "product-title").text
    try:
        status = soup.find("span", "gs-btn red color-only gient").text
        print("  .title : " + title)
        print("  .status : " + status)

        if (status == '품절'):  # 상품이 품절일 경우에만 return
            return {'title': title, 'status': status, 'link': url}
        return {'title': title, 'status': status, 'link': url}
    except:
        print("  .NoneType Error")  # 버튼의 형태가 바로구매, 품절이 아닌 다른 상태
        # return {'idx': self.idx, 'title': title, 'status': 'OtherStatus', 'link': url}


# @app은 아래 설정보다 위에 있어야 작동함
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
