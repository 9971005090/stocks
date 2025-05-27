# /utils/daum/constants.py
import sys

API = {
    'BASE': "https://finance.daum.net/api/",
    'QUOTES': "quotes/A{{ticker}}?summary=false&changeStatistics=true",
    'INVESTOR': "investor/days?page=1&perPage={{count}}&symbolCode=A{{ticker}}&pagination=true",
}