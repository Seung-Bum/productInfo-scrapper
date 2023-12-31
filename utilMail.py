import utilBase64
import os
import smtplib  # SMTP 사용을 위한 모듈
import re  # Regular Expression을 활용하기 위한 모듈
from email.mime.multipart import MIMEMultipart  # 메일의 Data 영역의 메시지를 만드는 모듈
from email.mime.text import MIMEText  # 메일의 본문 내용을 만드는 모듈
from email.mime.image import MIMEImage  # 메일의 이미지 파일을 base64 형식으로 변환하기 위한 모듈
from email.encoders import encode_base64
from email.header import Header
from email.mime.base import MIMEBase
from email.utils import formatdate


# 로그인 정보
my_account = utilBase64.decodingBase64('c2I5MTAxMjZAZ21haWwuY29t')
my_password = ""

# 메일을 받을 계정(입력받음)
to_mail = ""

# 메일 본문 내용
content = "안녕하세요. \n\n\
데이터를 전달드립니다.\n\n\
첨부파일 확인 부탁드립니다.\n\n\
감사합니다.\n\n\
"


def sendEmail(to_mail, token):
    my_password = token

    # smpt 서버와 연결
    gmail_smtp = "smtp.gmail.com"  # gmail smtp 주소
    gmail_port = 465  # gmail smtp 포트번호. 고정(변경 불가)
    smtp = smtplib.SMTP_SSL(gmail_smtp, gmail_port)

    smtp.login(my_account, my_password)

    # 메일 기본 정보 설정
    msg = MIMEMultipart()
    msg["Subject"] = f"첨부 파일 확인 바랍니다"  # 메일 제목
    msg["From"] = my_account
    msg["To"] = to_mail

    content_part = MIMEText(content, "plain")
    msg.attach(content_part)

    files = list()
    files.append('.\\productScrap.xlsx')
    # files.append('c:/projects/pylib/test.pdf')
    # files.append('c:/projects/pylib/test.jpg')

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f, "rb").read())
        encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    reg = "^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$"  # 유효성 검사를 위한 정규표현식
    if re.match(reg, to_mail):
        smtp.sendmail(my_account, to_mail, msg.as_string())
        print("  .정상적으로 메일이 발송되었습니다.")
        smtp.quit()
    else:
        print("  .받으실 메일 주소를 정확히 입력하십시오.")
        smtp.quit()


# 받는 메일 유효성 검사 거친 후 메일 전송
# sendEmail(to_mail)

# smtp 서버 연결 해제
# smtp.quit()

# 이미지 파일 추가
# image_name = "test.png"
# with open(image_name, 'rb') as file:
#     img = MIMEImage(file.read())
#     img.add_header('Content-Disposition', 'attachment', filename=image_name)
#     msg.attach(img)
