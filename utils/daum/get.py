
import os
import requests
import json
from utils.daum import constants as CONST
from utils import file as FILE
from datetime import datetime, timedelta

__all__ = ['RUN_USE_CHECK_FOR_DAUM']





# f'https://finance.daum.net/api/quotes/A{ticker}?summary=false&changeStatistics=true'
# f'https://finance.daum.net/api/investor/days?page=1&perPage=30&symbolCode=A{item}&pagination=true' (특정주식 상세 보기)
# f'https://finance.daum.net/api/investor/days?page=1&perPage=30&symbolCode=A{item}&pagination=true' (외국인/기관 매매 동향)
def _GET_NOW_INFO_FOR_DAUM(ticker):
    # url = f"{CONST.API['BASE']}{CONST.API['QUOTES']}".replace("{{ticker}}", ticker)
    url = f'https://finance.daum.net/api/quotes/A{ticker}?summary=false&changeStatistics=true'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Referer': f'http://finance.daum.net/quotes/A{ticker}',
    }
    r = requests.get(url, headers = headers)
    data = json.loads(r.text)
    return data
def _GET_DETAIL_INFO_FOR_DAUM(ticker, count = 30):
    url = f'https://finance.daum.net/api/investor/days?page=1&perPage={count}&symbolCode=A{ticker}&pagination=true'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Referer': f'http://finance.daum.net/quotes/A{ticker}',
    }
    r = requests.get(url, headers = headers)
    data = json.loads(r.text)
    return data


def _USE_CHECK_FOR_DAUM(ticker, name, date):
    data = _GET_NOW_INFO_FOR_DAUM(ticker)
    print("")
    print("=====date====")
    trades = _GET_DETAIL_INFO_FOR_DAUM(ticker)
    for trade in trades['data']:
        _date = trade['date'].replace("-", "")[0:8]
        if _date == date:
            data['recommendation_price'] = trade['tradePrice']
            break
    if data['market'] == "KOSPI":
        if data['marketCapRank'] <= 500:
            return (False, data)
    elif data['market'] == "KOSDAQ":
        if data['marketCapRank'] <= 250:
            return (False, data)
    return (True, data)


def RUN_CREATE_SIGNAL_TODAY_BUY_JSON(now_date = None):
    if now_date is None:
        now_date = datetime.now().strftime("%Y%m%d")
    return _CREATE_SIGNAL_TODAY_BUY_JSON(now_date)

def RUN_USE_CHECK_FOR_DAUM(ticker = None, name = None, date = None):
    if ticker is None or name is None or date is None:
        return (False, None)
    return _USE_CHECK_FOR_DAUM(ticker, name, date)

