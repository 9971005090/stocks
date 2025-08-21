
import os
import smtplib
import json
from email.mime.text import MIMEText
from utils import email as EMAIL

EMAIL.INIT()
EMAIL.SEND({"email": "9971005090@naver.com"}, "함수로 변경! 한 번 더!", "함수로 변경한 메일입니다.\n잘되겠죠?")

# 실행방법
'''
python3 -m python3 -m process.email.test_send_email
'''
