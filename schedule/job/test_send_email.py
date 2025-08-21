import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time
from schedule.shutdown import RUN as SCHEDULE_SHUTDOWN_RUN
from email.mime.text import MIMEText
from utils import email as EMAIL


"""Schedule the task for specific time on weekdays excluding holidays."""
SCHEDULER = BackgroundScheduler()

def schedule():
    EMAIL.INIT()
    EMAIL.SEND({"email": "9971005090@naver.com"}, "함수로 변경! 한 번 더!", "함수로 변경한 메일입니다.\n잘되겠죠?")

def SHUTDOWN_RUN():
    SCHEDULE_SHUTDOWN_RUN(SCHEDULER)

def RUN():
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':  # 실제 실행 중인 프로세스에서만 실행
        SCHEDULER.add_job(
            func=schedule,
            trigger='cron',
            second='*/10',
    #         minute='1-59',
            id='test_send_email_task',
        )

        SCHEDULER.start()
        print("Scheduler started. Waiting for the next execution...")