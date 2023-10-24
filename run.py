import time
from flask import Flask, render_template, request
from scrapper import productInfoExtract


# * 테스트 api 예시
#   린스 페이지 - http://localhost:5000/extract?param=1661646~1660624~1661646~404868~Sect-1661647-0-1
#
# * 403 ERROR -The request could not be satisfied.
#   위의 애러가 발생한 경우 GS홈쇼핑 페이지 크롤링 하다가 차단된 것임
#   시간이 지나면 차단된 것이 풀린다.


app = Flask(__name__)


# 카테고리당 한페이지로 sectid만 필요할듯함
@app.route("/extract", methods=['GET', 'POST'])
def productAllExtract():
    print("- productAllExtract START ---------------------------------")
    start = time.time()
    product_info_extract = productInfoExtract()
    sectid = request.args.get('sectid')
    print("  .sectid : " + sectid)

    title = product_info_extract.get_title(sectid)
    detailList = product_info_extract.get_product_status(sectid)
    end = time.time()
    print("- productAllExtract end ---------------------------------")
    print(f"{end - start:.5f} sec")
    return render_template(
        "report.html",
        title=title,
        rslt_list=detailList
    )


# @app은 아래 설정보다 위에 있어야 작동함
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


# @app.route('/')
# def home():
#     return 'This is home!'

# @app.route("/")
# def home():
#     return render_template("home.html")
