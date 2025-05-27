
import argparse
from utils import thinkpool as THINKPOOL

parser = argparse.ArgumentParser()
parser.add_argument('--date', default=None, help='날짜를 YYYYMMDD 형식으로 입력')
args = parser.parse_args()

THINKPOOL.RUN_CREATE_SIGNAL_TODAY_BUY_JSON(args.date)