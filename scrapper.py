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
    # 사용자가  입력값 (파라미터)
    mainUrl = request.args.get('mainUrl')

    mainSoup = make_soup(mainUrl)
    category_title = mainSoup.find("h2", "shop-title").get_text()
    prd_total_cnt = mainSoup.find("span", id="prd_cnt_").text  # 전체 상품수 카운트
    prd_total_cnt = int(re.sub(r'[^0-9]', '', prd_total_cnt))

    # 전체 상품수 / 한페이지의 상품 갯수 = 전체 페이지 (전체 페이지를 blind 해놔서 이렇게 구해야함)
    page_cnt = math.ceil(prd_total_cnt / 60)
    print('product_total: ' + str(prd_total_cnt))
    print('page_cnt: ' + str(page_cnt))

    return render_template("report.html", title=category_title, rslt_list=product_info_list)


# @app은 아래 설정보다 위에 있어야 작동함
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
