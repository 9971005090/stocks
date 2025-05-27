import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time
from schedule.shutdown import RUN as SCHEDULE_SHUTDOWN_RUN
from utils.day import _IS_WEEKDAY_ADN_NOT_HOLIDAY
from utils.thinkpool import _GET_THINKPOOL_SIGNAL_TODAY_BUY

"""Schedule the task for specific time on weekdays excluding holidays."""
SCHEDULER = BackgroundScheduler()


def SHUTDOWN_RUN():
    SCHEDULE_SHUTDOWN_RUN(SCHEDULER)

def RUN():
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':  # 실제 실행 중인 프로세스에서만 실행
        # Add a job that runs at 3:35 PM every day but only executes when conditions are met
        SCHEDULER.add_job(
            func=lambda: _GET_THINKPOOL_SIGNAL_TODAY_BUY() if _IS_WEEKDAY_ADN_NOT_HOLIDAY() else None,
            trigger='cron',
            hour=15,
            minute=54,
            id='weekday_task',
        )

        SCHEDULER.start()
        print("Scheduler started. Waiting for the next execution...")