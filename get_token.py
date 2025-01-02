import requests

url = 'https://kauth.kakao.com/oauth/token'
rest_api_key = '6fad03eb18f00f8d5957394608af9c2d'
redirect_uri = 'https://localhost:5000'
authorize_code = 'FtjHCDfxXRtxDHNh_iYlmd6dyPauSjh-RiN7qohaqgXLjC53Bx7TiQAAAAQKKcjZAAABk_dCOYvC3p98Pd5TpQ'

data = {
    'grant_type':'authorization_code',
    'client_id':rest_api_key,
    'redirect_uri':redirect_uri,
    'code': authorize_code,
    }

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)

# json 저장
import json
#1.
with open(r"./json/kakao_code.json","w") as fp:
    json.dump(tokens, fp)