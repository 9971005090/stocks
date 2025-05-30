
import os
import requests
import json
from utils.daum import constants as CONST
from utils import file as FILE
from datetime import datetime, timedelta

__all__ = ['RUN_USE_CHECK_FOR_DELETE', 'RUN_GET_STOCKS_FOR_DAILY', 'RUN_GET_STOCK_INFO']




def _CHECK_DATAS_UPTREND(datas, type = "daily"):
    if type == "daily":
        return (datas[-1] / datas[0]) > 1.02
    elif type == "weekly":
        return (datas[-1] / datas[0]) > 1.05
def _CHECK_BUYING_TREND(dicts, target_key, name = None):
    datas = [{"date": d["date"], "value": d[target_key]} for d in dicts]
    cumulative_sums = []
    total = 0

    for d in dicts:
        total += d.get(target_key, 0)
        cumulative_sums.append(total)

#     print()
#     print(name)
#     print(target_key)
#     print(cumulative_sums)

    # 우상향 판단: 누적 합계가 항상 이전 값보다 크거나 같은가?
    for i in range(1, len(cumulative_sums)):
        if cumulative_sums[i] < 0:
#             print("False")
            return (False, datas)
#     print("True")
    return (True, datas)


# f'https://finance.daum.net/api/quotes/A{ticker}?summary=false&changeStatistics=true'
# f'https://finance.daum.net/api/investor/days?page=1&perPage=30&symbolCode=A{item}&pagination=true' (특정주식 상세 보기)
# f'https://finance.daum.net/api/investor/days?page=1&perPage=30&symbolCode=A{item}&pagination=true' (외국인/기관 매매 동향)
def _GET_STOCK_INFO(ticker):
    # url = f"{CONST.API['BASE']}{CONST.API['QUOTES']}".replace("{{ticker}}", ticker)
    url = f'https://finance.daum.net/api/quotes/A{ticker}?summary=false&changeStatistics=true'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Referer': f'http://finance.daum.net/quotes/A{ticker}',
    }
    r = requests.get(url, headers = headers)
    data = json.loads(r.text)
    return data
def _GET_STOCKS_FOR_DAILY(ticker, count = 30):
    url = f'https://finance.daum.net/api/investor/days?page=1&perPage={count}&symbolCode=A{ticker}&pagination=true'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Referer': f'http://finance.daum.net/quotes/A{ticker}',
    }
    r = requests.get(url, headers = headers)
    data = json.loads(r.text)
    return data
def _GET_STOCKS_FOR_WEEKLY(ticker, count = 30):
    url = f'https://finance.daum.net/api/investor/weeks?page=1&perPage={count}&symbolCode=A{ticker}&pagination=true'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Referer': f'http://finance.daum.net/quotes/A{ticker}',
    }
    r = requests.get(url, headers = headers)
    data = json.loads(r.text)
    return data


def _USE_CHECK_FOR_DELETE(ticker, name, date):
    result = (True, None)
    data = _GET_STOCK_INFO(ticker)
    data['recommendation_price'] = data['tradePrice']
#     print()
#     print(f"name::::{data['name']}, per::::{data['per']}, pbr::::{data['pbr']}, dabtRatio:::{data['debtRatio']}, marketCapRank:::{data['marketCapRank']}")

    _c = (data['per'] is not None and data['per'] > 0 and data['per'] < 15) and (data['pbr'] is not None and data['pbr'] > 0 and data['pbr'] < 1.5) and (data['debtRatio'] is not None and data['debtRatio'] * 100 < 200)
    if _c is True:
        result = (False, data)
    if data['market'] == "KOSPI":
        if data['marketCapRank'] <= 500 and _c is True:
            result = (False, data)
    if data['market'] == "KOSDAQ":
        if data['marketCapRank'] <= 250 and _c is True:
            result = (False, data)

    if result[0] is False:
        trades = _GET_STOCKS_FOR_DAILY(ticker)
        for trade in trades['data']:
            _date = trade['date'].replace("-", "")[0:8]
            if _date == date:
                data['recommendation_price'] = trade['tradePrice']
                break

        # 외인/기관 매수량 우상향 판단
        _f, data['foreign_buying_trend'] = _CHECK_BUYING_TREND(trades['data'], 'foreignStraightPurchaseVolume', data['name'])
        _i, data['ins_buying_trend'] = _CHECK_BUYING_TREND(trades['data'], 'institutionStraightPurchaseVolume', data['name'])
        if _f is False and _i is False:
            result = (True, None)

    '''
    trades2 = _GET_STOCKS_FOR_WEEKLY(ticker)
    print()
    print(trades2)
    '''

    return result


def RUN_CREATE_SIGNAL_TODAY_BUY_JSON(now_date = None):
    if now_date is None:
        now_date = datetime.now().strftime("%Y%m%d")
    return _CREATE_SIGNAL_TODAY_BUY_JSON(now_date)

def RUN_USE_CHECK_FOR_DELETE(ticker = None, name = None, date = None):
    if ticker is None or name is None or date is None:
        return (False, None)
    return _USE_CHECK_FOR_DELETE(ticker, name, date)

def RUN_GET_STOCKS_FOR_DAILY(ticker = None):
    if ticker is None:
        return None
    return _GET_STOCKS_FOR_DAILY(ticker)

def RUN_GET_STOCK_INFO(ticker = None):
    if ticker is None:
        return None
    return _GET_STOCK_INFO(ticker)

