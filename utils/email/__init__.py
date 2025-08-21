import os
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

__all__ = ['INIT', 'SEND']

EMAIL = None

def INIT():
    global EMAIL
    EMAIL = json.loads(os.getenv("EMAIL_CONFIG"))

def SEND(to, subject, content, file_object = None):
    global EMAIL
    msg = MIMEText(content)
    if file_object != None:
        msg = MIMEMultipart()
        msg.attach(MIMEText(content, "plain"))
    msg["Subject"] = subject
    # msg["From"] = EMAIL['GMAIL']['ACCOUNT']['ADDRESS']
    msg["From"] = formataddr((EMAIL['GMAIL']['ACCOUNT']['ID'], EMAIL['GMAIL']['ACCOUNT']['ADDRESS']))
    msg["To"] = to['email']
    if file_object != None:
        msg.attach(file_object)

    # 이메일 보내기
    try:
        with smtplib.SMTP_SSL(EMAIL['GMAIL']['SMTP_SERVER']['URL'], EMAIL['GMAIL']['SMTP_SERVER']['PORT']) as server:
            server.login(EMAIL['GMAIL']['ACCOUNT']['ADDRESS'], EMAIL['GMAIL']['ACCOUNT']['PASSWORD'])
            server.sendmail(EMAIL['GMAIL']['ACCOUNT']['ADDRESS'], [msg["To"]], msg.as_string())
        return True
    except Exception as e:
        print("이메일 전송 실패:", e)
        return False