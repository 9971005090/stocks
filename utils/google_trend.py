import numpy as np
from pytrends.request import TrendReq
from pandas import Timestamp

# Google Trends API 클라이언트 초기화
pytrends = TrendReq(hl='ko', tz=540)

# 특정 키워드의 최근 7주간 국내 검색 트렌드 가져오기
def GET_KEYWORD_TREND(keyword, term):

    # 검색어 설정
    kw_list = [keyword]

    # 설정: 최근 7주, 대한민국 기준
    pytrends.build_payload(kw_list, cat=0, timeframe=f"{term['start']} {term['end']}", geo='KR', gprop='')

    # 관심도 시간대별 데이터 가져오기
    trends_data = pytrends.interest_over_time()

    result = []
    for date, interest in trends_data[[keyword]].iterrows():
        result.append({'date': date, 'interest': interest[keyword]})

    if not trends_data.empty:
        return _SERIALIZE_DATA(result)
    else:
        return None

def _SERIALIZE_DATA(data):
    for item in data:
        for key, value in item.items():  # 딕셔너리의 items() 호출
            if isinstance(value, Timestamp):
                item[key] = value.to_pydatetime().isoformat()  # ISO 8601 형식으로 변환
            if isinstance(value, np.integer): # np.int64를 확인
                item[key] = int(value)
    return data