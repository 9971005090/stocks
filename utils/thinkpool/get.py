
import os
import requests
import json
from utils.thinkpool import constants as CONST
from utils import file as FILE
from datetime import datetime, timedelta

__all__ = ['RUN_CREATE_SIGNAL_TODAY_BUY_JSON', 'RUN_READ_SIGNAL_TODAY_BUY_JSON']

# 라씨 매매 데이타 긁어와 json파일 만들기
def _CREATE_SIGNAL_TODAY_BUY_JSON(now_date):
    response = requests.get(f"{CONST.API['BASE']}{CONST.API['BUY']}")
    stocks = response.json()
    FILE.DELETE_IF_EXISTS(f"./json/stocks_{now_date}.json")
    with open(f"./json/stocks_{now_date}.json", "w") as fp:
        json.dump(stocks, fp, ensure_ascii=False, indent=4)
    return True


# 라씨 매매 저장된 데이타 json 긁어 오기
def _READ_SIGNAL_TODAY_BUY_JSON(date, root):
    TICKERS = None
    PATH = os.path.join(root, f"./json/stocks_{date}.json")
    print(PATH)
    # 파일 읽기 및 JSON 변환
    with open(PATH, "r", encoding="utf-8") as file:
        content = file.read()  # 파일 내용 읽기
        TICKERS = json.loads(content)  # JSON 문자열을 Python 객체로 변환
    return TICKERS

# def _SET_STOCK_PARSING(_TS, date):
#     TICKERS = []
#     for _T in _TS:
#         TICKERS.append({
#             'name': _T['daum_stock_info']['name'],
#             'code': _T['daum_stock_info']['symbolCode'].replace('A', ''),
#             'market': _T['daum_stock_info']['market'],
#             'recommendation_date': datetime.strptime(date, "%Y%m%d"),
#             'recommendation_price': _T['daum_stock_info']['recommendation_price'],
#             'rank': _T['daum_stock_info']['marketCapRank'],
#             'high_52_week': {
#                 'price': _T['daum_stock_info']['high52wPrice'],
#                 'date': datetime.strptime(_T['daum_stock_info']['high52wDate'], "%Y-%m-%d")
#             },
#             'high_50_day': {
#                 'price': _T['daum_stock_info']['high50dPrice'],
#             },
#             'low_52_week': {
#                 'price': _T['daum_stock_info']['low52wPrice'],
#                 'date': datetime.strptime(_T['daum_stock_info']['low52wDate'], "%Y-%m-%d")
#             },
#             'low_50_day': {
#                 'price': _T['daum_stock_info']['low50dPrice'],
#             },
#         })
#     return TICKERS
#
# def GET_STOCKS_BY_DATE(date):
#     TICKERS = []
#     _TS = _GET_THINKPOOL_SIGNAL_TODAY_JSON(date)
#     DELETE_TICKERS = []
#     delete = False
#     for _T in _TS:
#         delete, _T['daum_stock_info'] = _IS_DELETE_FOR_DAUM(_T['stockCode'].strip(), _T['stockName'], date)
#         if delete is True:
#             DELETE_TICKERS.append(_T)
#     for DELETE_TICKER in DELETE_TICKERS:
#         _TS.remove(DELETE_TICKER)
#     return _SET_STOCK_PARSING(_TS, date)
#
# def GET_NOW_INFO(ticker):
#     return _GET_NOW_INFO_FOR_DAUM(ticker)

def RUN_CREATE_SIGNAL_TODAY_BUY_JSON(now_date = None):
    if now_date is None:
        now_date = datetime.now().strftime("%Y%m%d")
    return _CREATE_SIGNAL_TODAY_BUY_JSON(now_date)

def RUN_READ_SIGNAL_TODAY_BUY_JSON(now_date = None, root = None):
    if now_date is None:
        now_date = datetime.now().strftime("%Y%m%d")
    if root is None:
        root = os.path.abspath(__file__)
    return _READ_SIGNAL_TODAY_BUY_JSON(now_date, root)

