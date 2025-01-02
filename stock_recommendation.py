import firebase_admin
import pandas as pd
import requests
import json
import os
from flask import Flask, jsonify, Response, request
from datetime import datetime, timedelta
from pykrx import stock
from flask_cors import CORS
from firebase_admin import credentials, firestore
from utils.thinkpool import GET_STOCKS_BY_DATE, GET_NOW_INFO
from utils.firebase import SERIALIZE_FIRESTORE_DATA, DOCUMENT_EXISTS
from utils.google_trend import GET_KEYWORD_TREND


APP = Flask(__name__)
TERM = 30
URL = 'https://api.thinkpool.com/signal/B/todayItemList'
END_DATE = datetime.now()
START_DATE = (END_DATE - timedelta(days=30))
PATH = f"./json/stocks_{END_DATE.strftime('%Y%m%d')}.json"
# STOCK = {
#     'KOSPI': stock.get_market_ticker_list(market="KOSPI"),
#     'KOSDAQ': stock.get_market_ticker_list(market="KOSDAQ"),
#     'TOTAL_KOSPI': None,
#     'TOTAL_KOSDAQ': None,
# }
TICKERS = None

# CORS 설정 추가
CORS(APP)

# 서비스 계정 키 JSON 경로
firebase_admin.initialize_app(credentials.Certificate("firebase/stock-a258d-firebase-adminsdk-b5cvc-ac46978ea8.json"))

# Firestore 데이터베이스 초기화
FIREBASE = {
    'DB_OBJECT': firestore.client(),
    'DB_COLLECTION_NAME': 'stocks'
}



# 시가 총액 구하기
def GET_TOTAL():
    global STOCK
    market_cap = stock.get_market_cap_by_ticker(date=END_DATE.strftime('%Y%m%d'))
    STOCK['TOTAL_KOSPI'] = market_cap.sort_values(by='시가총액', ascending=False)
    market_cap = stock.get_market_cap_by_ticker(date=END_DATE.strftime('%Y%m%d'), market="KOSDAQ")
    STOCK['TOTAL_KOSDAQ'] = market_cap.sort_values(by='시가총액', ascending=False)

    print(STOCK['KOSDAQ'])
    # market_rank = int(rank[ticker])


# 파일 여부 확인 후 삭제하기
def DELETE_FILE_IF_EXISTS(file_path):
    if os.path.exists(PATH):  # 파일이 존재하는지 확인
        os.remove(PATH)      # 파일 삭제

# 라씨 매매 데이타 긁어 오기
def GET_THINKPOOL_SIGNAL_TODAY_BUY():
    response = requests.get(URL)
    stocks = response.json()
    DELETE_FILE_IF_EXISTS(PATH)
    with open(PATH, "w") as fp:
        json.dump(stocks, fp, ensure_ascii=False, indent=4)

# 라씨 매매 저장된 데이타 json 긁어 오기
def GET_THINKPOOL_SIGNAL_TODAY_JSON():
    global TICKERS
    # 파일 읽기 및 JSON 변환
    with open(PATH, "r", encoding="utf-8") as file:
        content = file.read()  # 파일 내용 읽기
        TICKERS = json.loads(content)  # JSON 문자열을 Python 객체로 변환

# 코스피(1000위안), 코스닥(500위안) 인지 확인하고, 맞으면 False, 틀리면 True
def IS_DELETE(ticker):
    if ticker in STOCK['KOSPI']:
        if int(STOCK['TOTAL_KOSPI'][ticker]) <= 1000:
            return False
    elif ticker in STOCK['KOSDAQ']:
        if int(STOCK['TOTAL_KOSDAQ'][ticker]) <= 500:
            return False
    return True

def IS_DELETE_FOR_DAUM(ticker, name):
    url = f'https://finance.daum.net/api/quotes/A{ticker}?summary=false&changeStatistics=true'
    headers = {
                'Accept': 'application/json, text/plain, */*',
    #             'Accept-Encoding': 'gzip, deflate',
    #             'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    #             'Connection': 'keep-alive',
    #             'Cookie': 'GS_font_Name_no=0; GS_font_size=16; _ga=GA1.3.937989519.1493034297; webid=bb619e03ecbf4672b8d38a3fcedc3f8c; _ga=GA1.2.937989519.1493034297; _gid=GA1.2.215330840.1541556419; KAKAO_STOCK_RECENT=[%22A069500%22]; recentMenus=[{%22destination%22:%22chart%22%2C%22title%22:%22%EC%B0%A8%ED%8A%B8%22}%2C{%22destination%22:%22current%22%2C%22title%22:%22%ED%98%84%EC%9E%AC%EA%B0%80%22}]; TIARA=C-Tax5zAJ3L1CwQFDxYNxe-9yt4xuvAcw3IjfDg6hlCbJ_KXLZZhwEPhrMuSc5Rv1oty5obaYZzBQS5Du9ne5x7XZds-vHVF; webid_sync=1541565778037; _gat_gtag_UA_128578811_1=1; _dfs=VFlXMkVwUGJENlVvc1B3V2NaV1pFdHhpNTVZdnRZTWFZQWZwTzBPYWRxMFNVL3VrODRLY1VlbXI0dHhBZlJzcE03SS9Vblh0U2p2L2V2b3hQbU5mNlE9PS0tcGI2aXQrZ21qY0hFbzJ0S1hkaEhrZz09--6eba3111e6ac36d893bbc58439d2a3e0304c7cf3',
    #             'Host': 'finance.daum.net',
    #             'If-None-Match': 'W/"23501689faaaf24452ece4a039a904fd"',
                'Referer': f'http://finance.daum.net/quotes/A{ticker}',
    #             'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
                }
    r = requests.get(url, headers = headers)
    data = json.loads(r.text)
    if data['market'] == "KOSPI":
        if data['marketCapRank'] <= 500:
            return False
    elif data['market'] == "KOSDAQ":
        if data['marketCapRank'] <= 250:
            return False
    return True






# from bs4 import BeautifulSoup
#
# url = r'https://finance.naver.com/item/main.naver?code=289930'
#
# response = requests.get(url)
#
# if response.status_code == 200:
#     html = response.text
#     soup = BeautifulSoup(html, 'html.parser')
#     print(soup)
# else :
#     print(response.status_code)

# url = 'https://finance.daum.net/api/quotes/A289930?summary=false&changeStatistics=true'
# headers = {
#             'Accept': 'application/json, text/plain, */*',
# #             'Accept-Encoding': 'gzip, deflate',
# #             'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
# #             'Connection': 'keep-alive',
# #             'Cookie': 'GS_font_Name_no=0; GS_font_size=16; _ga=GA1.3.937989519.1493034297; webid=bb619e03ecbf4672b8d38a3fcedc3f8c; _ga=GA1.2.937989519.1493034297; _gid=GA1.2.215330840.1541556419; KAKAO_STOCK_RECENT=[%22A069500%22]; recentMenus=[{%22destination%22:%22chart%22%2C%22title%22:%22%EC%B0%A8%ED%8A%B8%22}%2C{%22destination%22:%22current%22%2C%22title%22:%22%ED%98%84%EC%9E%AC%EA%B0%80%22}]; TIARA=C-Tax5zAJ3L1CwQFDxYNxe-9yt4xuvAcw3IjfDg6hlCbJ_KXLZZhwEPhrMuSc5Rv1oty5obaYZzBQS5Du9ne5x7XZds-vHVF; webid_sync=1541565778037; _gat_gtag_UA_128578811_1=1; _dfs=VFlXMkVwUGJENlVvc1B3V2NaV1pFdHhpNTVZdnRZTWFZQWZwTzBPYWRxMFNVL3VrODRLY1VlbXI0dHhBZlJzcE03SS9Vblh0U2p2L2V2b3hQbU5mNlE9PS0tcGI2aXQrZ21qY0hFbzJ0S1hkaEhrZz09--6eba3111e6ac36d893bbc58439d2a3e0304c7cf3',
# #             'Host': 'finance.daum.net',
# #             'If-None-Match': 'W/"23501689faaaf24452ece4a039a904fd"',
#             'Referer': 'http://finance.daum.net/quotes/A069500',
# #             'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
#             }
# r = requests.get(url, headers = headers)
# data = json.loads(r.text)
#
# print(data)

@APP.route('/', methods=['GET'])
def index():
    # GET_TOTAL()
#     GET_THINKPOOL_SIGNAL_TODAY_BUY()
    GET_THINKPOOL_SIGNAL_TODAY_JSON()
    DELETE_TICKERS = []
    for TICKER in TICKERS:
        if IS_DELETE_FOR_DAUM(TICKER['stockCode'].strip(), TICKER['stockName']) is True:
            DELETE_TICKERS.append(TICKER)
    for DELETE_TICKER in DELETE_TICKERS:
        TICKERS.remove(DELETE_TICKER)
    print(TICKERS)
    return jsonify(TICKERS)

@APP.route('/<item>', methods=['GET'])
def detail(item):

    url = f'https://finance.daum.net/api/investor/days?page=1&perPage=30&symbolCode=A{item}&pagination=true'
    headers = {
                'Accept': 'application/json, text/plain, */*',
    #             'Accept-Encoding': 'gzip, deflate',
    #             'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    #             'Connection': 'keep-alive',
    #             'Cookie': 'GS_font_Name_no=0; GS_font_size=16; _ga=GA1.3.937989519.1493034297; webid=bb619e03ecbf4672b8d38a3fcedc3f8c; _ga=GA1.2.937989519.1493034297; _gid=GA1.2.215330840.1541556419; KAKAO_STOCK_RECENT=[%22A069500%22]; recentMenus=[{%22destination%22:%22chart%22%2C%22title%22:%22%EC%B0%A8%ED%8A%B8%22}%2C{%22destination%22:%22current%22%2C%22title%22:%22%ED%98%84%EC%9E%AC%EA%B0%80%22}]; TIARA=C-Tax5zAJ3L1CwQFDxYNxe-9yt4xuvAcw3IjfDg6hlCbJ_KXLZZhwEPhrMuSc5Rv1oty5obaYZzBQS5Du9ne5x7XZds-vHVF; webid_sync=1541565778037; _gat_gtag_UA_128578811_1=1; _dfs=VFlXMkVwUGJENlVvc1B3V2NaV1pFdHhpNTVZdnRZTWFZQWZwTzBPYWRxMFNVL3VrODRLY1VlbXI0dHhBZlJzcE03SS9Vblh0U2p2L2V2b3hQbU5mNlE9PS0tcGI2aXQrZ21qY0hFbzJ0S1hkaEhrZz09--6eba3111e6ac36d893bbc58439d2a3e0304c7cf3',
    #             'Host': 'finance.daum.net',
    #             'If-None-Match': 'W/"23501689faaaf24452ece4a039a904fd"',
                'Referer': f'http://finance.daum.net/quotes/A{item}',
    #             'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
                }
    r = requests.get(url, headers = headers)
    data = json.loads(r.text)
    return jsonify(data)  # JSON 응답


@APP.route('/rest', methods=['POST'])
def rest_index():
    # GET_TOTAL()
    #GET_THINKPOOL_SIGNAL_TODAY_BUY()
    GET_THINKPOOL_SIGNAL_TODAY_JSON()
    DELETE_TICKERS = []
    for TICKER in TICKERS:
        if IS_DELETE_FOR_DAUM(TICKER['stockCode'].strip(), TICKER['stockName']) is True:
            DELETE_TICKERS.append(TICKER)
    for DELETE_TICKER in DELETE_TICKERS:
        TICKERS.remove(DELETE_TICKER)
    response_json = json.dumps({'result': True, 'stocks': TICKERS}, ensure_ascii=False)
    return Response(response_json, content_type="application/json; charset=utf-8")
#     return jsonify(TICKERS), 200, {'Content-Type': 'application/json; charset=utf-8'}


@APP.route('/fb_add', methods=['GET'])
def firebase_add():
    def add_data():
        doc_ref = FIREBASE['DB_OBJECT'].collection('users').document('user_1')
        doc_ref.set({
            'name': '홍길동',
            'email': 'hong@example.com',
            'age': 30
        })
        print("데이터 추가 완료")
    add_data()

@APP.route('/fb_trend/<stock_name>/<term>', methods=['POST'])
def firebase_stock_trend(stock_name, term):
    term = int(term)
    _t = {
        'start': (END_DATE - timedelta(days=term)).strftime('%Y-%m-%d'),
        'end': END_DATE.strftime('%Y-%m-%d'),
    }
    response_json = json.dumps({'result': True, 'trend': GET_KEYWORD_TREND(stock_name, _t)}, ensure_ascii=False)
    return Response(response_json, content_type="application/json; charset=utf-8")

@APP.route('/fb_stocks', methods=['POST'])
def firebase_stock_index():
    stocks = []
#     docs = FIREBASE['DB_OBJECT'].collection(FIREBASE['DB_COLLECTION_NAME']).get()
    docs = FIREBASE['DB_OBJECT'].collection(FIREBASE['DB_COLLECTION_NAME']).order_by('recommendation_date').stream()

    # 모든 문서 출력
    for doc in docs:
        _d = doc.to_dict()
        _d['fb_id'] = doc.id
        _s = SERIALIZE_FIRESTORE_DATA(_d)
        _i = GET_NOW_INFO(_s['code'])
        _s['back_closing_price'] = _i['prevClosingPrice']       #전일 종가
        _s['trade_price'] = _i['tradePrice']                    #조회 시점의 가격(현재가)
        _s['company_info'] = _i['companySummary']               #회사 정보
        _s['chart'] = {                                         #주가 챠트
            "day": _i['chartImageUrl']['day'],
            "month": _i['chartImageUrl']['month'],
            "month3": _i['chartImageUrl']['month3'],
            "year": _i['chartImageUrl']['year'],
            "year3": _i['chartImageUrl']['year3'],
        }
        stocks.append(_s)
    response_json = json.dumps({'result': True, 'stocks': stocks}, ensure_ascii=False)
    return Response(response_json, content_type="application/json; charset=utf-8")

@APP.route('/fb_stocks/delete', methods=['POST'])
def firebase_stock_delete():
    data = request.json
    firebaseId = data.get("firebaseId")
    doc_ref = FIREBASE['DB_OBJECT'].collection(FIREBASE['DB_COLLECTION_NAME']).document(firebaseId)
    if doc_ref is None:
        response_json = json.dumps({'result': False, 'message': 'Information not found'}, ensure_ascii=False)
    else:
        doc_ref.delete()
        response_json = json.dumps({'result': True}, ensure_ascii=False)
    return Response(response_json, content_type="application/json; charset=utf-8")

@APP.route('/fb_stocks/update', methods=['POST'])
def firebase_stock_update():
    update_data = {}
    data = request.json
    firebaseId = data.get("firebaseId")
    column = data.get("column")
    value = data.get("value")
    doc_ref = FIREBASE['DB_OBJECT'].collection(FIREBASE['DB_COLLECTION_NAME']).document(firebaseId)
    if doc_ref is None:
        response_json = json.dumps({'result': False, 'message': 'Information not found'}, ensure_ascii=False)
    else:
        update_data[column] = value
        doc_ref.update(update_data)
        response_json = json.dumps({'result': True}, ensure_ascii=False)
    return Response(response_json, content_type="application/json; charset=utf-8")

@APP.route('/fb_stock_auto_add/', defaults={'date_string': '20241224'}, methods=['GET'])
@APP.route('/fb_stock_auto_add/<date_string>', methods=['GET'])
def firebase_stock_auto_add(date_string):
    stocks = GET_STOCKS_BY_DATE(date_string)
    for stock in stocks:
        _r = FIREBASE['DB_OBJECT'].collection(FIREBASE['DB_COLLECTION_NAME']).where('code', '==', stock['code']).stream()
        if DOCUMENT_EXISTS(_r) is False:
            FIREBASE['DB_OBJECT'].collection(FIREBASE['DB_COLLECTION_NAME']).add({
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
            })
    response_json = json.dumps({'result': True, 'message': '저장 완료'}, ensure_ascii=False)
    return Response(response_json, content_type="application/json; charset=utf-8")

# f'https://finance.daum.net/api/investor/days?page=1&perPage=30&symbolCode=A{item}&pagination=true' (특정주식 상세 보기)
# https://finance.daum.net/api/investor/days?page=1&perPage=30&symbolCode=A068270&pagination=true (외국인/기관 매매 동향)







if __name__ == '__main__':
#     root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#     print(root_directory)
#     # 루트 디렉토리에서 상대 경로로 파일 경로 만들기
#     file_path = os.path.join(root_directory, 'data', 'myfile.txt')
#     print(file_path)
#     GET_THINKPOOL_SIGNAL_TODAY_BUY()



    APP.run(debug=True, host='0.0.0.0', port=22222)