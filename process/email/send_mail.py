
import os
import smtplib
import json
from email.mime.text import MIMEText

# 환경 변수에서 가져오기
email = json.loads(os.getenv("EMAIL_CONFIG"))

# 이메일 메시지 만들기
msg = MIMEText("이것은 테스트 이메일입니다.")
msg["Subject"] = "테스트"
msg["From"] = email['GMAIL']['address']
msg["To"] = "9971005090@naver.com"

# 이메일 보내기
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email['GMAIL']['address'], email['GMAIL']['password'])
        server.sendmail(email['GMAIL']['address'], [msg["To"]], msg.as_string())
    print("이메일 전송 성공")
except Exception as e:
    print("이메일 전송 실패:", e)

# 실행방법
'''
python3 -m python3 -m process.email.send_mail
'''
