from flask import Blueprint
from custom.firebase import FIREBASE

STOCKS_BLUEPRINT = Blueprint('stocks', __name__)

@STOCKS_BLUEPRINT.route('/stocks', methods=['POST'])
def get_stocks():
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