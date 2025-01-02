
from datetime import datetime
from .daum import _IS_DELETE_FOR_DAUM, _GET_NOW_INFO_FOR_DAUM
import json

# 라씨 매매 저장된 데이타 json 긁어 오기
def _GET_THINKPOOL_SIGNAL_TODAY_JSON(date):
    TICKERS = None
    PATH = f"./json/stocks_{date}.json"
    # 파일 읽기 및 JSON 변환
    with open(PATH, "r", encoding="utf-8") as file:
        content = file.read()  # 파일 내용 읽기
        TICKERS = json.loads(content)  # JSON 문자열을 Python 객체로 변환
    return TICKERS

def _SET_STOCK_PARSING(_TS, date):
    TICKERS = []
    for _T in _TS:
        TICKERS.append({
            'name': _T['daum_stock_info']['name'],
            'code': _T['daum_stock_info']['symbolCode'].replace('A', ''),
            'market': _T['daum_stock_info']['market'],
            'recommendation_date': datetime.strptime(date, "%Y%m%d"),
            'recommendation_price': _T['daum_stock_info']['recommendation_price'],
            'rank': _T['daum_stock_info']['marketCapRank'],
            'high_52_week': {
                'price': _T['daum_stock_info']['high52wPrice'],
                'date': datetime.strptime(_T['daum_stock_info']['high52wDate'], "%Y-%m-%d")
            },
            'high_50_day': {
                'price': _T['daum_stock_info']['high50dPrice'],
            },
            'low_52_week': {
                'price': _T['daum_stock_info']['low52wPrice'],
                'date': datetime.strptime(_T['daum_stock_info']['low52wDate'], "%Y-%m-%d")
            },
            'low_50_day': {
                'price': _T['daum_stock_info']['low50dPrice'],
            },
        })
    return TICKERS

def GET_STOCKS_BY_DATE(date):
    TICKERS = []
    _TS = _GET_THINKPOOL_SIGNAL_TODAY_JSON(date)
    DELETE_TICKERS = []
    delete = False
    for _T in _TS:
        delete, _T['daum_stock_info'] = _IS_DELETE_FOR_DAUM(_T['stockCode'].strip(), _T['stockName'], date)
        if delete is True:
            DELETE_TICKERS.append(_T)
    for DELETE_TICKER in DELETE_TICKERS:
        _TS.remove(DELETE_TICKER)
    return _SET_STOCK_PARSING(_TS, date)

def GET_NOW_INFO(ticker):
    return _GET_NOW_INFO_FOR_DAUM(ticker)

