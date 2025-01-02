

from google.cloud.firestore_v1._helpers import DatetimeWithNanoseconds

def SERIALIZE_FIRESTORE_DATA(data):
    for key, value in data.items():
        if isinstance(value, DatetimeWithNanoseconds):
            data[key] = value.isoformat()  # ISO 8601 형식으로 변환
    return data

def DOCUMENT_EXISTS(datas):
    for _ in datas:
        return True
    return False

