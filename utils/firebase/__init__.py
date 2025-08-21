import json
import os
import firebase_admin
from firebase_admin import credentials, initialize_app, firestore
from google.cloud.firestore_v1._helpers import DatetimeWithNanoseconds
from google.cloud.firestore_v1 import FieldFilter

__all__ = ['INFO', 'INIT', 'SERIALIZE_FIRESTORE_DATA', 'DOCUMENT_EXISTS', 'FieldFilter', 'ADD_COLLECTION']

INFO = {
    'DB_OBJECT': None,
    'DB_COLLECTION_NAME': None,
    'DB_COLLECTION': {}
}

def INIT(stocks_name = 'stocks'):
    global INFO

    if not firebase_admin._apps:
        # 서비스 계정 키 JSON 경로
        # initialize_app(credentials.Certificate("firebase/stock-a258d-firebase-adminsdk-b5cvc-ac46978ea8.json"))
        initialize_app(credentials.Certificate(json.loads(os.getenv('FIREBASE_CONFIG'))))

    # Firestore 데이터베이스 초기화
    INFO['DB_OBJECT'] = firestore.client()
    INFO['DB_COLLECTION_NAME'] = stocks_name
    INFO['DB_COLLECTION'][stocks_name] = stocks_name

def ADD_COLLECTION(name):
    global INFO
    INFO['DB_COLLECTION'][name] = name

def SERIALIZE_FIRESTORE_DATA(data):
    for key, value in data.items():
        if isinstance(value, DatetimeWithNanoseconds):
            data[key] = value.isoformat()  # ISO 8601 형식으로 변환
    return data

def DOCUMENT_EXISTS(datas):
    for _ in datas:
        return True
    return False