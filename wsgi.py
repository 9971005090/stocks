# wsgi.py
from stock_recommendation import APP  # stock_recommendation.py에서 정의한 Flask 앱을 import

if __name__ == "__main__":
    APP.run()