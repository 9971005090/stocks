
import sys
import os
import argparse
from datetime import datetime, time
from google.cloud.firestore_v1.base_query import FieldFilter
from utils import firebase as FIREBASE
from utils import thinkpool as THINKPOOL

parser = argparse.ArgumentParser()
parser.add_argument('--date', default=None, help='날짜를 YYYYMMDD 형식으로 입력')
args = parser.parse_args()

if args.date is None:
    args.date = datetime.now().strftime("%Y%m%d")

FB_COLLECTION = {}
FB_COLLECTION['STOCKS_JSON'] = "stocks_json"
FIREBASE.ADD_COLLECTION(FB_COLLECTION['STOCKS_JSON'])

# firebase에서 해당날짜 조회
target = datetime.strptime(args.date, "%Y%m%d").isoformat()
docs = FIREBASE.INFO['DB_OBJECT'].collection(FIREBASE.INFO['DB_COLLECTION'][FB_COLLECTION['STOCKS_JSON']]).where(filter=FieldFilter("created_at", "==", target)).stream()

for doc in docs:
    value = doc.to_dict()

THINKPOOL.RUN_SAVE_SIGNAL_CHOICE_DATE_BUY_STOCKS_TO_FIREBASE(args.date, value['stocks'])

