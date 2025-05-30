
from __init__ import __version__
from flask import Flask, jsonify
from utils import firebase as FIREBASE
from utils import cors as CORS
from api import api_bp

APP = Flask(__name__)
FIREBASE.INIT()
APP.register_blueprint(api_bp)
CORS.SETUP(APP)

if __name__ == '__main__':
    APP.run(debug=True, host='0.0.0.0', port=22222)