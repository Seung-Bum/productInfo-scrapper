from flask import Flask, render_template, request
from scrapper import productInfoExtract


# * 테스트 api 예시
#   린스 페이지 - http://localhost:5000/extract?param=1661646~1660624~1661646~404868~Sect-1661647-0-1
#
# * 403 ERROR -The request could not be satisfied.
#   위의 애러가 발생한 경우 GS홈쇼핑 페이지 크롤링 하다가 차단된 것임
#   시간이 지나면 차단된 것이 풀린다.


app = Flask(__name__)


# 카테고리 한페이지
# sectid만 필요할듯함
@app.route("/extract", methods=['GET', 'POST'])
def productAllExtract():
    print("- productAllExtract START ---------------------------------")
    product_info_extract = productInfoExtract()
    param_list = []
    sectid = {}

    # 자동으로 url 인코딩이 안되는 '~'를 구분자로 넣어 파라미터 넘김
    param = request.args.get('param')
    splitParam = str(param).split("~")
    sectid["sectid"] = splitParam[0]
    sectid["lsectid"] = splitParam[1]
    sectid["msectid"] = splitParam[2]
    sectid["lseq"] = splitParam[3]
    sectid["gsid"] = splitParam[4]
    param_list.extend([sectid["sectid"], sectid["lsectid"],
                      sectid["msectid"], sectid["lseq"], sectid["gsid"]])

    print("  .sectid : " + sectid["sectid"])
    print("  .lsectid : " + sectid["lsectid"])
    print("  .msectid : " + sectid["msectid"])
    print("  .lseq : " + sectid["lseq"])
    print("  .gsid : " + sectid["gsid"])

    # 리스트안에 리스트 담김
    detailList = product_info_extract.get_product_status(param_list)

    print("  .productAllExtract end ---------------------------------")
    return render_template(
        "report.html",
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
