import os
import json
import io
from pytz import timezone
from email.mime.base import MIMEBase
from email import encoders
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time
from schedule.shutdown import RUN as SCHEDULE_SHUTDOWN_RUN
from utils.date import _IS_WEEKDAY_AND_NOT_HOLIDAY
from utils.thinkpool import RUN_GET_SIGNAL_TODAY_BUY as THINKPOOL_RUN_GET_SIGNAL_TODAY_BUY
from utils import email as EMAIL
from utils import file as FILE
from utils import firebase as FIREBASE

"""Schedule the task for specific time on weekdays excluding holidays."""
SCHEDULER = BackgroundScheduler()

FB_COLLECTION = {}
FB_COLLECTION['STOCKS_JSON'] = "stocks_json"

def send_email(response):
    EMAIL.INIT()
    subject = f'[씽크풀] {datetime.now().strftime("%Y년 %m월 %d")} 매수 정보'
    content = json.dumps(response, indent=4, ensure_ascii=False)
    attachment = FILE.GET_JSON_ATTACHMENT(response, f'{datetime.now().strftime("thinkpool_buy_%Y%m%d")}.json')
    EMAIL.SEND({"email": "9971005090@naver.com"}, subject, content, attachment)

def save_firebase(response):
    now = datetime.now()
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

def schedule():
    now = datetime.now()
    print(f"✅ thinkpool_buy_add_send_email_save_firebase 스케줄러 실행 {now.strftime('%Y년 %m월 %d일  %H시 %M분 %S초')} {_IS_WEEKDAY_AND_NOT_HOLIDAY()}")
    if _IS_WEEKDAY_AND_NOT_HOLIDAY() == True:
        response = THINKPOOL_RUN_GET_SIGNAL_TODAY_BUY()
        send_email(response)
        save_firebase(response)

def SHUTDOWN_RUN():
    SCHEDULE_SHUTDOWN_RUN(SCHEDULER)

def RUN():
    print(f'✅ thinkpool_buy_add_send_email_save_firebase 스케줄러 등록 완료')
    is_local = os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
    is_render = os.environ.get('RENDER') is not None  # Render 환경에서 자동 설정됨
    if is_local or is_render:
        SCHEDULER.add_job(
            func=schedule,
            trigger='cron',
#             second=0,
#             minute='1-59',
<<<<<<< Updated upstream
            hour=16,       # 오후 4시
            minute=30,      # 0분
            second=0,      # 0초
=======
            hour=9,
            minute=30,
            second=0,
>>>>>>> Stashed changes
            timezone=timezone('Asia/Seoul'),  # 한국 시간대 지정
            id='stocks_send_email_save_firebase_task',
        )

        SCHEDULER.start()
        print("Scheduler started. Waiting for the next execution...")
