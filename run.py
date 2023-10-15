import requests
from flask import Flask, render_template, request, redirect, send_file
from scrapper import extract_Status, get_product_status
from urllib import parse

app = Flask(__name__)

# @app.route('/')
# def home():
#     return 'This is home!'


@app.route("/")
def home():
    return render_template("home.html")


# 페이지 하나의 결과를 추출하는 메서드
@app.route("/report")
def report():
    rslt_list = []

    # 사용자가 검색한 값 (파라미터(상품아이디)), request에 담겨서 전달됨
    prdid = request.args.get('prdid')

    if prdid:
        html = 'https://www.gsshop.com/prd/prd.gs?prdid=' + prdid
        print('html : ' + html)

        # 상품 상태값 추출 (바로구매, 품절)
        rslt_dict = extract_Status(html)
        print(rslt_dict)

        # 결과들을 dict에 담아서 전달
        rslt_list.append(rslt_dict)
    else:
        return redirect("/")
    return render_template(
        "report.html",
        rslt_list=rslt_list
    )
    # report.html에 각각의 값을 넘겨준다. render


# 카테고리 한페이지
@app.route("/test", methods=['GET', 'POST'])
def productAllExtract():
    print("- productAllExtract START")
    param_list = []
    sectid = {}

    # 자동으로 url 인코딩이 안되는 '-'를 구분자로 넣어 파라미터 넘김
    param = request.args.get('param')
    splitParam = str(param).split("~")
    sectid["sectid"] = splitParam[0]
    sectid["lsectid"] = splitParam[1]
    sectid["msectid"] = splitParam[2]
    sectid["lseq"] = splitParam[3]
    sectid["gsid"] = splitParam[4]
    param_list.extend([sectid["sectid"], sectid["lsectid"],
                      sectid["msectid"], sectid["lseq"], sectid["gsid"]])

    print("sectid : " + sectid["sectid"])
    print("lsectid : " + sectid["lsectid"])
    print("msectid : " + sectid["msectid"])
    print("lseq : " + sectid["lseq"])
    print("gsid : " + sectid["gsid"])
    detailList = get_product_status(param_list)
    print("  .productAllExtract detailList complete, html render start")
    return render_template(
        "report.html",
        rslt_list=detailList
    )


# @app은 아래 설정보다 위에 있어야 작동함
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
