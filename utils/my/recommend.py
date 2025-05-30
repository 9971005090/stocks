import yfinance as yf
from konlpy.tag import Okt
from collections import Counter
from transformers import pipeline
import requests
from bs4 import BeautifulSoup

# --- 1. 보수적 재무 조건 판별 함수 ---
def conservative_stock_filter(ticker):
    stock = yf.Ticker(ticker)
    print(stock.info)
    info = stock.info

    # 필수 지표들 (예시로 yfinance info에 없는 경우 None 처리)
    per = info.get('trailingPE')
    pbr = info.get('priceToBook')
#     roe = info.get('returnOnEquity')
    debt_ratio = None

    # 부채비율은 info에 안 나오는 경우 많아, 재무재표로 찾아도 됨 (여기선 대략 None 처리)
    # 필요시 별도 재무제표 파싱 추가 가능

    # 보수적 조건
    conditions = [
        per is not None and per < 15,       # PER < 15
        pbr is not None and pbr < 1.5,      # PBR < 1.5
#         roe is not None and roe > 0.15,     # ROE > 15%
        debt_ratio is None or debt_ratio < 100,  # 부채비율 < 100% (미확인시 pass)
    ]
    passed = all(conditions)
    return passed, {'PER': per, 'PBR': pbr, 'ROE': roe, 'DebtRatio': debt_ratio}


# # --- 2. 주가 추세 판단 함수 ---
# def check_price_trend(ticker):
#     stock = yf.Ticker(ticker)
#     hist = stock.history(period="2mo", interval="1d")  # 일봉 2개월치
#     hist_weekly = stock.history(period="5mo", interval="1wk")  # 주봉 5개월치
#
#     # 최근 15일 일봉 상승 판단: 15일치 종가 직전값들로 일별 상승여부 판단
#     recent_15_close = hist['Close'][-15:]
#     daily_diff = recent_15_close.diff().dropna()
#     daily_uptrend = (daily_diff > 0).all()
#
#     # 최근 4주 주봉 상승 판단: 4주치 종가 직전값 상승 판단
#     recent_4week_close = hist_weekly['Close'][-4:]
#     weekly_diff = recent_4week_close.diff().dropna()
#     weekly_uptrend = (weekly_diff > 0).all()
#
#     return daily_uptrend, weekly_uptrend

# 2) 최근 15일간 일봉 상승 여부 체크
def check_daily_uptrend(ticker, days=15):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo", interval="1d")  # 일봉 1개월치
    recent_15_close = hist['Close'][days*-1:]

    return (recent_15_close[-1] / recent_15_close[0]) > 1.02

# 3) 최근 4주간 주봉 상승 여부 체크
def check_weekly_uptrend(ticker, weeks=4):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="5mo", interval="1wk")  # 주봉 5개월치
    recent_4week_close = hist_weekly['Close'][-4:]

    return (recent_4week_close[-1] > recent_4week_close[0]) > 1.05