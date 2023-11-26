import time
from flask import Flask, render_template, request, redirect
from scrapper import productInfoExtract

# * 웹서버로 실행시 main.py를 통해 실행
# * 403 ERROR -The request could not be satisfied.
#   위의 애러가 발생한 경우 GS홈쇼핑 페이지 크롤링 하다가 차단된 것임
#   시간이 지나면 차단된 것이 풀린다.

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


# methods=['GET', 'POST']
@app.route("/extract")
def productAllExtract():
    param = {}
    sectid = request.args.get('sectid')
    to_mail = request.args.get('toMail')

    param['sectid'] = sectid
    param['to_mail'] = to_mail

    print("setid : " + str(sectid))
    print("to_mail : " + str(to_mail))
    productInfoExtract().productAllExtract(param, 'web')

# def productAllExtract():
#     print("- productAllExtract START ---------------------------------")
#     start = time.time()
#     sectid = request.args.get('sectid')
#     product_info_extract = productInfoExtract()
#     if sectid:
#         print("  .sectid : " + str(sectid))
#         title = product_info_extract.get_title(sectid)
#         detailList = product_info_extract.get_product_status(sectid)
#     else:
#         print("  .sectid : NONE")
#         return redirect("/")
#     end = time.time()
#     print("- productAllExtract end ---------------------------------")
#     print(f"{end - start:.2f} sec")
#     return render_template("report.html", title=title, rslt_list=detailList)


# @app은 아래 설정보다 위에 있어야 작동함
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

# @app.route('/')
# def home():
#     return 'This is home!'

# @app.route("/report")
# def report():
#   #사용자가 검색한 값 (파라미터), request에 담겨서 전달됨
#   word = request.args.get('word')
