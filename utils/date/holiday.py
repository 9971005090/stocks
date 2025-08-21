from datetime import datetime, time
import holidays
import importlib
from datetime import datetime

year = datetime.now().year
module_name = f"utils.date.temp_holiday_{year}"   # 예: date.temp_holiday_2025

mod = importlib.import_module(module_name)
TEMP_HOLIDAYS = mod.TEMP_HOLIDAYS


def _GET_HOLIDAY(nation = 'kr'):
    if (nation == 'kr'):
        return holidays.KR()
    return holidays.KR()

def _IS_WEEKDAY_AND_NOT_HOLIDAY():
    KOREA_HOLIDAYS = _GET_HOLIDAY()
    today = datetime.now().date()
    return today.weekday() < 5 and today not in KOREA_HOLIDAYS and today not in TEMP_HOLIDAYS