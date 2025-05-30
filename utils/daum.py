

import json
import requests

# f'https://finance.daum.net/api/quotes/A{ticker}?summary=false&changeStatistics=true'
# f'https://finance.daum.net/api/investor/days?page=1&perPage=30&symbolCode=A{item}&pagination=true' (특정주식 상세 보기)
# f'https://finance.daum.net/api/investor/days?page=1&perPage=30&symbolCode=A{item}&pagination=true' (외국인/기관 매매 동향)
def _GET_NOW_INFO_FOR_DAUM(ticker):
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


def _IS_DELETE_FOR_DAUM(ticker, name, date):
    data = _GET_NOW_INFO_FOR_DAUM(ticker)
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
    # _IS_DELETE_FOR_DAUM_DETAIL(ticker)
    return (True, data)

def _IS_DELETE_FOR_DAUM_DETAIL(ticker):
    url = f'https://finance.daum.net/api/investor/days?page=1&perPage=30&symbolCode=A{ticker}&pagination=true'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Referer': f'http://finance.daum.net/quotes/A{ticker}',
    }
    r = requests.get(url, headers = headers)
    data = json.loads(r.text)
    print("\n\n\n")
    print(f"""
        코드: {ticker}\n
        내용: {data}
    """)
    print("\n\n\n")

'''
{
   "symbolCode":"A034230",                                          #사용자주식코드
   "code":"KR7034230003",                                           #거래서내부주식코드
   "name":"파라다이스",                                                #이름
   "market":"KOSPI",                                                #거래소구분
   "isIndex":false,
   "openingPrice":9560.0,                                           #시가
   "highPrice":9700.0,                                              #고가
   "lowPrice":9500.0,                                               #저가
   "tradePrice":9690.0,                                             #조회한 시점의 현재가
   "prevClosingPrice":9590.0,                                       #전일종가
   "change":"RISE",                                                 #조회한 시점의 변동 구분
   "changePrice":100.0,                                             #조회한 시점의 변동 가격
   "changeRate":0.0104275287,                                       #조회한 시점의 변동률
   "accTradePrice":222638940.0,                                     #조회한 시점의 거래대금
   "accTradeVolume":23156,                                          #조회한 시점의 거래량
   "prevAccTradeVolume":103687,
   "prevAccTradeVolumeChangeRate":0.2233259714,
   "basePrice":9590.0,
   "upperLimitPrice":12460.0,
   "lowerLimitPrice":6720.0,
   "date":"2024-12-30",
   "tradeDate":"20241230",
   "tradeTime":"094500",
   "timestamp":1735519500000,
   "exchangeDate":"2024-12-30 09:45:00",
   "exchangeLocalType":"None",
   "exchangeCountry":"KOREA",
   "exchange":"None",
   "currency":"KRW",
   "high52wPrice":15710.0,                                          #52주 신고가
   "high52wDate":"2024-05-02",                                      #52주 신고가 날짜
   "low52wPrice":9000.0,                                            #52주 신저가
   "low52wDate":"2024-11-15",                                       #52주 신저가 날짜
   "high50dPrice":10720.0,                                          #50일 신고가
   "low50dPrice":9560.0,                                            #50일 신저가
   "highInYearPrice":15710.0,                                       #24년 신고가
   "lowInYearPrice":9000.0,                                         #24년 신저가
   "earlyYearPrice":"None",
   "lastWeekPrice":"None",
   "sectorCode":"None",
   "sectorName":"None",
   "sectorChangeRate":0.0,
   "sectorPer":102.11701,                                           #해당 업종의 평균 per
   "wicsSectorCode":"G253010",
   "wicsSectorName":"호텔,레스토랑,레저",
   "wicsSectorChangeRate":-0.0026795253,
   "marketCap":889267026870,
   "marketCapRank":259,
   "foreignRatio":0.0496624757,
   "prevForeignRatio":"None",
   "foreignOwnShares":4557606,
   "eps":725.0,
   "bps":16278.0,
   "dps":100.0,
   "per":13.23,                                                     #해당 회상의 per
   "pbr":0.59,
   "companySummary":"동사는 1972년 4월 27일 설립되었으며, 2002년 11월 5일자로 코스닥시장에 상장되어 코스닥시장에서 매매거래가 개시됨. 동사는 4개의 외국인전용 카지노 사업장을 운영하고 있으며, 연결기준 카지노 부문에는 서울, 부산, 제주 카지노가 포함됨. 복합리조트 부문에서는 인천 영종도의 '파라다이스시티' 리조트가 속해 있으며, 이 안에는 카지노, 호텔, 기타 엔터테인먼트 시설이 있음.",
   "debtRatio":0.96748,                                             #해당 회사의 부채비율
   "sales":268244966330.0,
   "operatingProfit":36204836500.0,
   "preTaxProfit":20869060150.0,
   "netIncome":19662276490.0,
   "askPrice":9700,
   "bidPrice":9690,
   "securityGroup":"STOCK",
   "parValue":500.0,
   "listedShareCount":91771623,
   "listingDate":"2024-06-24",
   "settleMonth":12,
   "capitalStock":47446830500.0,
   "isDelisted":false,
   "stockState":{
      "isBackDoorListed":false,
      "marketWarning":"NONE",
      "isTradingSuspended":false,
      "parValueChange":"NONE",
      "isUnfaithfulDisclosureDesignated":false,
      "ex":"NONE",
      "isAdministrativeIssue":false,
      "revaluation":"NONE",
      "isPreDelistingTrading":false,
      "isLowLiquidity":false,
      "isDelisted":false
   },
   "investorSummary":{
      "individualStraightPurchasePrice":"None",
      "institutionStraightPurchasePrice":"None",
      "foreignStraightPurchasePrice":"None",
      "programStraightPurchasePrice":"None"
   },
   "signedChangeRate5daysAgo":"None",
   "signedChangeRate20daysAgo":"None",
   "signedChangeRate60daysAgo":"None",
   "signedChangeRate120daysAgo":"None",
   "signedChangeRate250daysAgo":"None",
   "prevClosingPrice5daysAgo":"None",
   "prevClosingPrice20daysAgo":"None",
   "prevClosingPrice60daysAgo":"None",
   "prevClosingPrice120daysAgo":"None",
   "prevClosingPrice250daysAgo":"None",
   "isClosing":false,
   "changeStatistics":"None",
   "chartImageUrl":{
      "day":"https://t1.daumcdn.net/media/finance/chart/kr/daumstock/d/A034230.png",
      "month":"https://t1.daumcdn.net/media/finance/chart/kr/daumstock/m/A034230.png",
      "month3":"https://t1.daumcdn.net/media/finance/chart/kr/daumstock/m3/A034230.png",
      "year":"https://t1.daumcdn.net/media/finance/chart/kr/daumstock/y/A034230.png",
      "year3":"https://t1.daumcdn.net/media/finance/chart/kr/daumstock/y3/A034230.png"
   },
   "chartSlideImage":"None"
}

{
   "date":"2024-12-27 00:00:00",                            #날짜
   "foreignOwnShares":193157,                               #외인보유주식수
   "foreignOwnSharesRate":0.0111329683,                     #외인보유지분
   "foreignStraightPurchaseVolume":32800,                   #외인순매수량
   "institutionStraightPurchaseVolume":-56609,              #기관순매수량
   "institutionCumulativeStraightPurchaseVolume":-56609,    #?
   "tradePrice":9920.0,                                     #종가
   "changePrice":30.0,                                      #전일비
   "change":"RISE",                                         #등락률
   "accTradeVolume":99616,                                  #거래량
   "accTradePrice":988865540.0                              #거래금액
}
'''