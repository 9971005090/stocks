from flask import Flask, jsonify
from pykrx import stock
import requests
import pandas as pd


app = Flask(__name__)

# 특정 URL에 접속하여 JSON 데이터를 받아오는 함수
def get_json_from_url(url):
    # GET 요청을 보냄
    response = requests.get(url)

    # 응답이 성공적인지 확인
    if response.status_code == 200:
        return response.json()  # JSON 파싱 후 반환
    else:
        return None  # 오류 발생 시 None 반환

@app.route('/')
def index():
#     url = "https://api.thinkpool.com/signal/B/todayItemList"  # 여기에 실제 API URL을 입력하세요
#
#     # URL에서 JSON 데이터 받아오기
#     data = get_json_from_url(url)
#
#     if data:
#         # 객체 배열의 내용을 하나씩 출력
#         for item in data:
#             print(item)  # 데이터 출력
#         return jsonify(data)  # JSON 응답을 반환
#     else:
#         return jsonify({"error": "Failed to fetch data"}), 500


    # 종목 코드와 기간 설정
    ticker = "005930"  # 삼성전자의 종목 코드
    start_date = "20231101"  # 시작 날짜 (예시: 최근 한 달)
    end_date = "20231120"  # 종료 날짜 (예시: 최근 한 달)

    # 주식 데이터 가져오기 (시가, 고가, 저가, 종가, 거래량, 외국인 매수량 포함)
    df = stock.get_market_ohlcv(start_date, end_date, ticker)
    print(df)

    return "hi"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=22222)
