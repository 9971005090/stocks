
import os
import argparse
from utils import daum as DAUM

parser = argparse.ArgumentParser()
parser.add_argument('--ticker', default=None, help='숫자 6자리')
args = parser.parse_args()

#result = MY.conservative_stock_filter(args.ticker)
result = DAUM.RUN_GET_STOCKS_FOR_DAILY(args.ticker)
print(result)

# 095660.KQ
'''
yfinance는 기본적으로 미국 시장 종목을 대상으로 합니다.
한국 종목을 조회하려면 티커에 .KS 또는 .KQ를 붙여야 합니다.
'''