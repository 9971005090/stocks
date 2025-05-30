
import json
from flask import Response
from utils import firebase as FIREBASE
from utils import daum as DAUM

def register(bp):
    @bp.route('/stocks/list', methods=['GET', 'POST'])
    def get_stocks():

        stocks = []
    #     docs = FIREBASE['DB_OBJECT'].collection(FIREBASE['DB_COLLECTION_NAME']).get()
        docs = FIREBASE.INFO['DB_OBJECT'].collection(FIREBASE.INFO['DB_COLLECTION_NAME']).order_by('recommendation_date').stream()

        # 모든 문서 출력
        for doc in docs:
            _d = doc.to_dict()
            _d['fb_id'] = doc.id
            _s = FIREBASE.SERIALIZE_FIRESTORE_DATA(_d)
            _i = DAUM.RUN_GET_STOCK_INFO(_s['code'])
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
