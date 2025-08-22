
import os
import json
import io
from pytz import timezone
from email.mime.base import MIMEBase
from email import encoders
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time
from zoneinfo import ZoneInfo
from schedule.shutdown import RUN as SCHEDULE_SHUTDOWN_RUN
from utils.date import _IS_WEEKDAY_AND_NOT_HOLIDAY
from utils.thinkpool import RUN_GET_SIGNAL_TODAY_BUY as THINKPOOL_RUN_GET_SIGNAL_TODAY_BUY
from utils import email as EMAIL
from utils import file as FILE
from utils import firebase as FIREBASE

FB_COLLECTION = {}
FB_COLLECTION['STOCKS_JSON'] = "stocks_json"
def send_email(response):
    EMAIL.INIT()
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    subject = f'[씽크풀] {now.strftime("%Y년 %m월 %d")} 매수 정보'
    content = json.dumps(response, indent=4, ensure_ascii=False)
    attachment = FILE.GET_JSON_ATTACHMENT(response, f'{now.strftime("thinkpool_buy_%Y%m%d")}.json')
    EMAIL.SEND({"email": "9971005090@naver.com"}, subject, content, attachment)

def save_firebase(response):
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    today = datetime(now.year, now.month, now.day, 0, 0, 0).isoformat()
    FIREBASE.ADD_COLLECTION(FB_COLLECTION['STOCKS_JSON'])
    _r = FIREBASE.INFO['DB_OBJECT'].collection(FIREBASE.INFO['DB_COLLECTION'][FB_COLLECTION['STOCKS_JSON']]).where(filter=FIREBASE.FieldFilter('created_at', '==', today)).stream()
    if FIREBASE.DOCUMENT_EXISTS(_r) is False:
        doc_id = f"{now.strftime('%Y%m%d')}"
        doc_data = []
        for stock in response:
#             FIREBASE.INFO['DB_OBJECT'].collection(FIREBASE.INFO['DB_COLLECTION'][FB_COLLECTION['STOCKS_JSON']]).add({
#                 'stockCode': stock['stockCode'],
#                 'stockName': stock['stockName'],
#                 'tradeFlag': stock['tradeFlag'],
#                 'elapsedTmTx': stock['elapsedTmTx'],
#                 'timeFlag': stock['timeFlag'],
#                 'tradePrice': stock['tradePrice'],
#                 'created_at': today,
#             })
            doc_data.append({
                'stockCode': stock['stockCode'],
                'stockName': stock['stockName'],
                'tradeFlag': stock['tradeFlag'],
                'elapsedTmTx': stock['elapsedTmTx'],
                'timeFlag': stock['timeFlag'],
                'tradePrice': stock['tradePrice'],
                'created_at': today,
            })

        FIREBASE.INFO['DB_OBJECT'].collection(FIREBASE.INFO['DB_COLLECTION'][FB_COLLECTION['STOCKS_JSON']]).document(doc_id).set({
            "stocks": doc_data,
            "created_at": today
        })
    return True

if _IS_WEEKDAY_AND_NOT_HOLIDAY() == True:
    response = THINKPOOL_RUN_GET_SIGNAL_TODAY_BUY()
    print(response)
    send_email(response)
    save_firebase(response)

