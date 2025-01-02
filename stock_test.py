from pykrx import stock
import pandas as pd

def get_stock_details(ticker: str):
    # 오늘 날짜 계산
    today = pd.Timestamp.today().strftime("%Y%m%d")

    # 1. 코스피/코스닥 구분
    market_type = "코스피" if ticker in stock.get_market_ticker_list(market="KOSPI") else "코스닥"

    # 2. 시가총액 순위
    market_cap = stock.get_market_cap_by_ticker(date=today)
    rank = market_cap["시가총액"].rank(ascending=False)
    market_rank = int(rank[ticker])

    # 3. 최근 20 영업일 데이터 가져오기
    end_date = today
    start_date = (pd.Timestamp.today() - pd.Timedelta(days=30)).strftime("%Y%m%d")

    # 외국인 매매량 가져오기
    volume = stock.get_market_trading_volume_by_date(start_date, end_date, ticker)
#     if foreign_volume.shape[1] == 1:
#         foreign_volume.columns = ["외국인 매매량"]  # 컬럼 이름 변경 (하나일 경우)

#     # 기관 매매량 가져오기
#     institution_volume = stock.get_market_trading_volume_by_date(start_date, end_date, ticker, "기관")
#     if institution_volume.shape[1] == 1:
#         institution_volume.columns = ["기관 매매량"]  # 컬럼 이름 변경 (하나일 경우)
#
#     # 기관 누적 순매매량 계산
#     institution_cumulative = institution_volume.cumsum()
#     if institution_cumulative.shape[1] == 1:
#         institution_cumulative.columns = ["기관 누적 순매매량"]  # 컬럼 이름 변경 (하나일 경우)

#     # 종가 및 거래량 가져오기
#     daily_price = stock.get_market_ohlcv_by_date(start_date, end_date, ticker)[['종가', '거래량']]

#     # 데이터 병합 시 중복되는 컬럼 이름을 방지하기 위해 DataFrame으로 변환
#     merged_data = pd.concat([foreign_volume, institution_volume, institution_cumulative, daily_price], axis=1).tail(20)

    print(volume)

    df = stock.get_market_cap(start_date, end_date, ticker)
    df_d = df.to_dict()
    print(df_d['시가총액'])
#     for item in df_d['시가총액'].items():
#         print(item[0].strftime('%Y%m%d'))
#         print(type(item[0]))
#     # 결과 출력
#     print(f"종목코드: {ticker}")
#     print(f"시장구분: {market_type}")
#     print(f"시가총액 순위: {market_rank}")
#     print(f"최근 20 영업일 상세정보:\n{merged_data}")
#     return merged_data

# 예제: 삼성전자 (005930)
# result = get_stock_details("005930")

# 예제: 셀트리온 (068270)
result = get_stock_details("068270")
