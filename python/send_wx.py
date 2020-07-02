import requests
import json


def get_access_token():
    result = requests.get(
        url="https://api.weixin.qq.com/cgi-bin/token",
        params={
            "grant_type": "client_credential",
            "appid": "xxxx",
            "secret": "xxxx",
        }
    ).json()

    if result.get("access_token"):
        access_token = result.get('access_token')
    else:
        access_token = None
    return access_token

def sendmsg(openid,msg):

    access_token = get_access_token()

    body = {
        "touser": openid,
        "msgtype": "text",
        "text": {
            "content": msg
        }
    }
    response = requests.post(
        url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
        params={
            'access_token': access_token
        },
        data=bytes(json.dumps(body, ensure_ascii=False), encoding='utf-8')
    )
    result = response.json()
    print(result)



if __name__ == '__main__':
    sendmsg('xxxx','xxxx')