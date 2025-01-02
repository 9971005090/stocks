import requests
import json
import pandas as pd
import time
from utils.thinkpool import GET_STOCKS_BY_DATE

def get_stock_details(ticker: str):
    date_string = "20241224"
    stocks = GET_STOCKS_BY_DATE(date_string)
    return stocks

# 예제: 셀트리온 (068270)

start_time = time.time()  # 시작 시간
result = get_stock_details("068270")
end_time = time.time()    # 종료 시간
execution_time = end_time - start_time
print(f"\n\n처리 시간: {execution_time:.2f} 초")


# f'https://finance.daum.net/api/investor/days?page=1&perPage=30&symbolCode=A{item}&pagination=true' (특정주식 상세 보기)