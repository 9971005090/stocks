import json
import os
from firebase_admin import credentials, initialize_app, firestore

INFO = {
    'DB_OBJECT': None,
    'DB_COLLECTION_NAME': None
}

def INIT(stocks_name = 'stocks'):
    global INFO

    if not firebase_admin._apps:
        # 서비스 계정 키 JSON 경로
        # initialize_app(credentials.Certificate("firebase/stock-a258d-firebase-adminsdk-b5cvc-ac46978ea8.json"))
        initialize_app(credentials.Certificate(json.loads(os.getenv('FIREBASE_CONFIG'))))

    # Firestore 데이터베이스 초기화
    INFO = {
        'DB_OBJECT': firestore.client(),
        'DB_COLLECTION_NAME': stocks_name
    }