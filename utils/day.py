from datetime import datetime, time
import holidays

def _GET_HOLIDAY(nation = 'kr'):
    if (nation == 'kr'):
        return holidays.KR()
    return holidays.KR()

def _IS_WEEKDAY_ADN_NOT_HOLIDAY():
    KOREA_HOLIDAYS = _GET_HOLIDAY()
    today = datetime.now().date()
    return today.weekday() < 5 and today not in KOREA_HOLIDAYS  # 0-4 are Mon-Fri