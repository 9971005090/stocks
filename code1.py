from flask import Flask, jsonify, request
import json
import requests
import webbrowser

app = Flask(__name__)

@app.route('/')
def index():
    # 사용자 인증 URL 생성
    client_id = "6126028584a8fe8f6320a92572a1f363"
    redirect_uri = "http://localhost:5000/oauth"
    scope = "talk_message"  # 카카오톡 메시지 전송 권한
    url = f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}"

    # 브라우저 열기
    webbrowser.open(url)

    return "hi"

@app.route('/oauth')
def oauth():
    # URL 쿼리 파라미터에서 'code'를 받기
    code = request.args.get('code')
    if code:
        # 액세스 토큰 요청
        token_url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": "6126028584a8fe8f6320a92572a1f363",
            "redirect_uri": "http://localhost:5000/oauth",
            "code": code  # 브라우저에서 받은 코드 입력
        }
        response = requests.post(token_url, data=data)
        tokens = response.json()
        print(tokens)
        if tokens:
            # 액세스 토큰 (OAuth 인증 후 발급받은 토큰 입력)
            ACCESS_TOKEN = tokens['access_token']

            # 메시지 데이터 (템플릿 메시지 예제)
            headers = {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": "application/json"  # 수정된 부분
            }

            data = {
                "template_object": {
                    "object_type": "text",
                    "text": "안녕하세요, 나와의 채팅 테스트입니다!",
                    "link": {
                        "web_url": "https://developers.kakao.com",
                        "mobile_web_url": "https://developers.kakao.com"
                    },
                    "button_title": "확인"
                }
            }

            response = requests.post(
                "https://kapi.kakao.com/v2/api/talk/memo/default/send",
                headers=headers,
                data=json.dumps(data)
            )

            # 응답 처리
            if response.status_code == 200:
                print("메시지 전송 성공!")
            else:
                print(f"메시지 전송 실패: {response.status_code}")
                print(response.json())
        return tokens

    return "oauth"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)