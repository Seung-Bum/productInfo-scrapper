import requests
from flask import Flask, render_template, request, redirect, send_file
from scrapper import extract_Status, get_product_status

app = Flask(__name__)

# @app.route('/')
# def home():
#     return 'This is home!'


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
    rslt_list = []

    # 사용자가 검색한 값 (파라미터), request에 담겨서 전달됨
    prdid = request.args.get('prdid')

    if prdid:
        html = 'https://www.gsshop.com/prd/prd.gs?prdid=' + prdid
        print('html : ' + html)

        rslt_dict = extract_Status(html)
        print(rslt_dict)

        rslt_list.append(rslt_dict)
    else:
        return redirect("/")
    return render_template(
        "report.html",
        rslt_list=rslt_list
    )
    # report.html에 각각의 값을 넘겨준다. render


@app.route("/test", methods=['GET', 'POST'])
def test():
    endpoint = request.args.get('endpoint')

    print("fist : " + endpoint)
    return get_product_status(endpoint)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
