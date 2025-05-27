
import os
import argparse
from STOCKS.utils import thinkpool as THINKPOOL

parser = argparse.ArgumentParser()
parser.add_argument('--date', default=None, help='날짜를 YYYYMMDD 형식으로 입력')
args = parser.parse_args()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TICKERS = THINKPOOL.RUN_SAVE_SIGNAL_TODAY_BUY_TO_FIREBASE(args.date, ROOT)
print(TICKERS)