
import sys
import os
import json
import argparse
from datetime import datetime, time
from zoneinfo import ZoneInfo
from google.cloud.firestore_v1.base_query import FieldFilter
from utils import firebase as FIREBASE
from utils import thinkpool as THINKPOOL
from utils import email as EMAIL
from utils import file as FILE
from utils.date import _IS_WEEKDAY_AND_NOT_HOLIDAY

def send_email(response, choice_date):
    EMAIL.INIT()
    target = datetime.strptime(choice_date, "%Y%m%d")
#     now = datetime.now(ZoneInfo("Asia/Seoul"))
    target.replace(tzinfo=ZoneInfo("Asia/Seoul"))
    subject = f'[씽크풀 추천 분류] {target.strftime("%Y년 %m월 %d")} 매수 정보 - 추천 분류'
    content = json.dumps(response, indent=4, ensure_ascii=False)
    attachment = FILE.GET_JSON_ATTACHMENT(response, f'{target.strftime("thinkpool_recommand_buy_%Y%m%d")}.json')
    EMAIL.SEND({"email": "9971005090@naver.com"}, subject, content, attachment)

parser = argparse.ArgumentParser()
parser.add_argument('--date', default=None, help='날짜를 YYYYMMDD 형식으로 입력')
args = parser.parse_args()

if args.date is None:
    args.date = datetime.now().strftime("%Y%m%d")

FB_COLLECTION = {}
FB_COLLECTION['STOCKS_JSON'] = "stocks_json"
FIREBASE.ADD_COLLECTION(FB_COLLECTION['STOCKS_JSON'])

if _IS_WEEKDAY_AND_NOT_HOLIDAY() == True:
    # firebase에서 해당날짜 조회
    target = datetime.strptime(args.date, "%Y%m%d").isoformat()
    docs = FIREBASE.INFO['DB_OBJECT'].collection(FIREBASE.INFO['DB_COLLECTION'][FB_COLLECTION['STOCKS_JSON']]).where(filter=FieldFilter("created_at", "==", target)).stream()

    for doc in docs:
        value = doc.to_dict()

    THINKPOOL.RUN_SAVE_SIGNAL_CHOICE_DATE_BUY_STOCKS_TO_FIREBASE(args.date, value['stocks'])

    send_email(value['stocks'], args.date)