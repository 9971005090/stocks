from pytrends.request import TrendReq

# Google Trends API 클라이언트 초기화
pytrends = TrendReq(hl='ko', tz=540)

# 특정 키워드의 최근 7주간 국내 검색 트렌드 가져오기
def get_keyword_trend(keyword):
    # 검색어 설정
    kw_list = [keyword]

    # 설정: 최근 7주, 대한민국 기준
    pytrends.build_payload(kw_list, cat=0, timeframe='2024-12-01 2024-12-31', geo='KR', gprop='')

    # 관심도 시간대별 데이터 가져오기
    trends_data = pytrends.interest_over_time()

    if not trends_data.empty:
        # 관심도 출력
        print(f"최근 7주간 '{keyword}'의 관심도:")
#         print(trends_data[[keyword]])
        for date, interest in trends_data[[keyword]].iterrows():
            print(f"Date: {date}, Interest: {interest[keyword]}")
        return trends_data[[keyword]]
    else:
        print(f"'{keyword}'에 대한 데이터가 없습니다.")
        return None

# 키워드 검색
get_keyword_trend("롯데에너지머티리얼즈")