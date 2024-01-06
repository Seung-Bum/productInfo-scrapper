from scrapper_web import get_product_info_class_web
from flask import Flask, render_template, request
from utilExcel import makeExcel
from utilMail import sendEmail
# from scrapper import productInfoExtract

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


# methods=['GET', 'POST']
@app.route("/extract")
def productAllExtract():
    # 사용자가  입력값 (파라미터)
    sectid = request.args.get('sectid')
    to_mail = request.args.get('email')

    param = {}
    param['sectid'] = sectid
    param['to_mail'] = to_mail
    print("setid : " + str(sectid))
    print("to_mail : " + str(to_mail))
    product_info_list, category_title = get_product_info_class_web().get_product_page(param)
    makeExcel(category_title, product_info_list)
    sendEmail(to_mail)
    return render_template("report.html", rslt_list=product_info_list, title=category_title)


# @app은 아래 설정보다 위에 있어야 작동함
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
