from flask import Flask, jsonify, request
import json
import requests
import webbrowser

app = Flask(__name__)

@app.route('/oauth')
def oauth():
    # URL 쿼리 파라미터에서 'code'를 받기
    code = request.args.get('code')
    if code:
        return code
    else:
        return "fail"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)