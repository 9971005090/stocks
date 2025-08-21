
import requests
import json
from utils.thinkpool import constants as CONST
from utils.thinkpool import get as GET
from utils.daum import get as DAUM_GET
from utils import file as FILE
from datetime import datetime, timedelta
from utils import firebase as FIREBASE

FIREBASE.INIT()

__all__ = ['RUN_SAVE_SIGNAL_TODAY_BUY_TO_FIREBASE']


def _SET_STOCK_PARSING(_TS, date):
    TICKERS = []
    for _T in _TS:
        # 'recommendation_price': _T['daum_stock_info']['recommendation_price'],
        TICKERS.append({
            'name': _T['daum_stock_info']['name'],
            'code': _T['daum_stock_info']['symbolCode'].replace('A', ''),
            'market': _T['daum_stock_info']['market'],
            'per': _T['daum_stock_info']['per'],
            'pbr': _T['daum_stock_info']['pbr'],
            'debt_ratio': _T['daum_stock_info']['debtRatio'],
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
            'foreign_buying_trend': _T['daum_stock_info']['foreign_buying_trend'],
            'ins_buying_trend': _T['daum_stock_info']['ins_buying_trend'],
        })
    return TICKERS

# 라씨 매수 JSON 파일에서 데이타를 긁어와, firebase에 저장
def _SAVE_SIGNAL_TODAY_BUY_TO_FIREBASE(date, root):
    DELETE_TICKERS = []
    _TS = GET.RUN_READ_SIGNAL_TODAY_BUY_JSON(date, root)
    delete = False
    for _T in _TS:
        delete, _T['daum_stock_info'] = DAUM_GET.RUN_USE_CHECK_FOR_DELETE(_T['stockCode'].strip(), _T['stockName'], date)
        if delete is True:
            DELETE_TICKERS.append(_T)
    for DELETE_TICKER in DELETE_TICKERS:
        _TS.remove(DELETE_TICKER)
    stocks = _SET_STOCK_PARSING(_TS, date)
    for stock in stocks:
        print()
        print(stock)
    for stock in stocks:
        _r = FIREBASE.INFO['DB_OBJECT'].collection(FIREBASE.INFO['DB_COLLECTION_NAME']).where(filter=FIREBASE.FieldFilter('code', '==', stock['code'])).stream()
        if FIREBASE.DOCUMENT_EXISTS(_r) is False:
            FIREBASE.INFO['DB_OBJECT'].collection(FIREBASE.INFO['DB_COLLECTION_NAME']).add({
                'name': stock['name'],
                'code': stock['code'],
                'market': stock['market'],
                'recommendation_date': stock['recommendation_date'],
                'recommendation_price': stock['recommendation_price'],
                'rank': stock['rank'],
                'high_52_week_price': stock['high_52_week']['price'],
                'high_52_week_date': stock['high_52_week']['date'],
                'low_52_week_price': stock['low_52_week']['price'],
                'low_52_week_date': stock['low_52_week']['date'],
                'high_50_day_price': stock['high_50_day']['price'],
                'low_50_day_price': stock['low_50_day']['price'],
                'buy_date': None,
                'average_price': None,
                'per': stock['per'],
                'pbr': stock['pbr'],
                'debt_ratio': stock['debt_ratio'] * 100,
                'foreign_buying_trend': stock['foreign_buying_trend'],
                'ins_buying_trend': stock['ins_buying_trend'],
            })
    return True

# 라씨 매수 JSON 파일에서 데이타를 긁어와, firebase에 저장
def _SAVE_SIGNAL_TODAY_BUY_ORIGINAL_TO_FIREBASE(date):
    with open(f"./json/stocks_{now_date}.json", "w") as fp:
            json.dump(stocks, fp, ensure_ascii=False, indent=4)
    return True

def RUN_SAVE_SIGNAL_TODAY_BUY_TO_FIREBASE(now_date = None, root = None):
    if now_date is None:
        now_date = datetime.now().strftime("%Y%m%d")
    return _SAVE_SIGNAL_TODAY_BUY_TO_FIREBASE(now_date, root)

def RUN_SAVE_SIGNAL_TODAY_BUY_ORIGINAL_TO_FIREBASE(now_date = None):
    if now_date is None:
        now_date = datetime.now().strftime("%Y%m%d")
    return _SAVE_SIGNAL_TODAY_BUY_ORIGINAL_TO_FIREBASE(now_date)

