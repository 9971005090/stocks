from PyKakao import Message
import requests

# 카카오 REST API 키를 입력하세요
REST_API_KEY = "6fad03eb18f00f8d5957394608af9c2d"
REDIRECT_URI = "YOUR_REDIRECT_URI"  # Redirect URI (Kakao Developers에서 설정한 값)
ACCESS_TOKEN = None  # 액세스 토큰

# Kakao 객체 초기화
MSG = Message(REST_API_KEY)

def check_token_validity(access_token):
    url = "https://kapi.kakao.com/v1/user/access_token_info"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    print(response.json())


# 1. OAuth를 통한 사용자 인증
def login():
    auth_url = MSG.get_url_for_generating_code()
    print(f"다음 URL로 이동하여 인증을 완료하세요: {auth_url}")

    # 인증 완료 후 Kakao Developers에서 설정한 Redirect URI로 이동됩니다.
    # 이동한 URI에서 `code` 파라미터를 복사해 가져오세요.
    code = input("인증 후 반환된 code를 입력하세요: ")

    # 카카오 인증코드 발급 URL 접속 후 리다이렉트된 URL
    url = "https://localhost:5000/"

    global ACCESS_TOKEN
    # 위 URL로 액세스 토큰 추출
    ACCESS_TOKEN = MSG.get_access_token_by_code(code)

    # 액세스 토큰 설정
    MSG.set_access_token(ACCESS_TOKEN)
    print("액세스 토큰:", ACCESS_TOKEN)
    check_token_validity(ACCESS_TOKEN)

    # 1. 나에게 보내기 API - 텍스트 메시지 보내기 예시
    message_type = "text" # 메시지 유형 - 텍스트
    text = "텍스트 영역입니다. 최대 200자 표시 가능합니다." # 전송할 텍스트 메시지 내용

    MSG.send_message_to_me(
        message_type=message_type,
        text=text
    )


# 2. 메시지 보내기
def send_message():
    if not ACCESS_TOKEN:
        print("로그인 후 액세스 토큰을 설정하세요.")
        return

    # 전송할 메시지 내용
    message = {
        "object_type": "text",
        "text": "안녕하세요, PyKakao로 보낸 메시지입니다!",
        "link": {
            "web_url": "https://example.com",
            "mobile_web_url": "https://example.com"
        },
        "button_title": "더 보기"
    }

    # 메시지 전송 (친구 ID나 그룹 ID를 지정해야 함)
    try:
        response = kakao.send_message(receiver_id='USER_ID', message=message)
        print("메시지 전송 성공:", response)
    except Exception as e:
        print("메시지 전송 실패:", e)

# 실행 순서
if __name__ == "__main__":
    print("1. 로그인 진행")
    login()
#
#     print("\n2. 메시지 보내기")
#     send_message()