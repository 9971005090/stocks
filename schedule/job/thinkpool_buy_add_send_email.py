import os
import json
import io
from email.mime.base import MIMEBase
from email import encoders
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time
from schedule.shutdown import RUN as SCHEDULE_SHUTDOWN_RUN
from utils.day import _IS_WEEKDAY_ADN_NOT_HOLIDAY
from utils.thinkpool import RUN_GET_SIGNAL_TODAY_BUY as THINKPOOL_RUN_GET_SIGNAL_TODAY_BUY
from utils import email as EMAIL
from utils import file as FILE

"""Schedule the task for specific time on weekdays excluding holidays."""
SCHEDULER = BackgroundScheduler()

def schedule():
    response = THINKPOOL_RUN_GET_SIGNAL_TODAY_BUY()
    EMAIL.INIT()
    subject = f'[씽크풀] {datetime.now().strftime("%Y년 %m월 %d")} 매수 정보'
    content = json.dumps(response, indent=4, ensure_ascii=False)
    attachment = FILE.GET_JSON_ATTACHMENT(response, f'{datetime.now().strftime("thinkpool_buy_%Y%m%d")}.json')
    EMAIL.SEND({"email": "9971005090@naver.com"}, subject, content, attachment)

def SHUTDOWN_RUN():
    SCHEDULE_SHUTDOWN_RUN(SCHEDULER)

def RUN():
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':  # 실제 실행 중인 프로세스에서만 실행
        SCHEDULER.add_job(
            func=schedule,
            trigger='cron',
            second=0,
    #         minute='1-59',
            id='test_send_email_task',
        )

        SCHEDULER.start()
        print("Scheduler started. Waiting for the next execution...")