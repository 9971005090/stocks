
import requests
import json
from datetime import datetime
from .daum import _IS_DELETE_FOR_DAUM, _GET_NOW_INFO_FOR_DAUM


__all__ = ['RUN_SAVE_SIGNAL_TODAY_BUY_TO_FIREBASE']



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