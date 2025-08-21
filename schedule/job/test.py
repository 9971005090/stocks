import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time
from schedule.shutdown import RUN as SCHEDULE_SHUTDOWN_RUN

"""Schedule the task for specific time on weekdays excluding holidays."""
SCHEDULER = BackgroundScheduler()

def schedule_print():
    print("\n\n")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def SHUTDOWN_RUN():
    SCHEDULE_SHUTDOWN_RUN(SCHEDULER)

def RUN():
#     if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':  # 실제 실행 중인 프로세스에서만 실행
#         # Add a job that runs at 3:35 PM every day but only executes when conditions are met
#         SCHEDULER.add_job(
#             func=schedule_print,
#             trigger='cron',
#             minute='1-59',
#             id='weekday_task',
#         )
#
#         SCHEDULER.start()
#         print("Scheduler started. Waiting for the next execution...")
# Add a job that runs at 3:35 PM every day but only executes when conditions are met
    SCHEDULER.add_job(
        func=schedule_print,
        trigger='cron',
        second='*/10',
#         minute='1-59',
        id='weekday_task',
    )

    SCHEDULER.start()
    print("Scheduler started. Waiting for the next execution...")


if __name__ == "__main__":
    RUN()
    try:
        while True:
            pass  # 혹은 time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        SCHEDULER.shutdown()