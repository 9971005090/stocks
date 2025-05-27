
import pandas as pd
import requests
import json
import os
from flask import Flask, jsonify, Response, request
from datetime import datetime, timedelta
from pykrx import stock
from flask_cors import CORS
from utils.thinkpool import GET_STOCKS_BY_DATE, GET_NOW_INFO, _GET_THINKPOOL_SIGNAL_TODAY_BUY
from utils.firebase import SERIALIZE_FIRESTORE_DATA, DOCUMENT_EXISTS
from utils.google_trend import GET_KEYWORD_TREND
# from schedule.job.test import RUN as SCHEDULE_JOB_TEST_RUN, SHUTDOWN_RUN
from schedule.job.thinkpool_add import RUN as SCHEDULE_JOB_THINKPOOL_ADD_RUN, SHUTDOWN_RUN as JOB_THINKPOOL_ADD_SHUTDOWN_RUN
from custom.firebase import INIT as CUSTOM_FIREBASE_INIT, FIREBASE


_GET_THINKPOOL_SIGNAL_TODAY_BUY()