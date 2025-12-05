import base64
import hashlib
import json

import requests

from requests_toolbelt import MultipartEncoder
def webhook_wx(webhook_url, content, image_path=None):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "msgtype": "text",
        "text": {
            "content": content,
            # "mentioned_list": ["@all"],
        }
    }
    data = json.dumps(data).encode('utf-8')
    response = requests.post(webhook_url, headers=headers, data=data)
    res_json = response.json()
    if image_path:
        image = open(image_path, 'rb').read()
        image_base64 = str(base64.b64encode(image), 'utf-8')
        image_md5 = hashlib.md5(image).hexdigest()
        data = {
            "msgtype": "image",
            "image": {
                "base64": image_base64,
                "md5": image_md5
            }
        }
        data = json.dumps(data).encode('utf-8')
        response = requests.post(webhook_url, headers=headers, data=data)
        image_res_json = response.json()
    data = {
        "msgtype": "text",
        "text": {
            "content": '================================',
        }
    }
    data = json.dumps(data).encode('utf-8')
    response = requests.post(webhook_url, headers=headers, data=data)
    res_json = response.json()
    return res_json

def webhook_lark(webhook_url, content, image_path=None):
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = {
        'msg_type': 'text',
        'content': {
            'text': content,
        },
    }
    response = requests.post(webhook_url, headers=headers, json=json_data)
    res_json = response.json()
    if image_path:
        image_res = upload_image2lark(image_path)
        image_key = image_res['data']['image_key']
        json_data = {
            "msg_type": "image",
            "content": {
                "image_key": image_key
            }
        }
        response = requests.post(webhook_url, headers=headers, json=json_data)
        image_res_json = response.json()
    json_data = {
        'msg_type': 'text',
        'content': {
            'text': '================================',
        },
    }
    response = requests.post(webhook_url, headers=headers, json=json_data)
    res_json = response.json()
    return res_json


def get_lark_token(app_id='cli_a74389c055bd900d', app_secret='2z0sbJsANyCPn2QPz24LObpqFg3oIgVg'):
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
    }
    json_data = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    response = requests.post(url, headers=headers, json=json_data)
    res_json = response.json()
    return res_json

def upload_image2lark(image_path):
    token = get_lark_token()
    tenant_access_token = token['tenant_access_token']
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    form = {
        'image_type': 'message',
        'image': (open(image_path, 'rb'))
    }
    multi_form = MultipartEncoder(form)
    headers = {
        'Authorization': f'Bearer {tenant_access_token}',
        'Content-Type': multi_form.content_type
    }
    response = requests.post(url, headers=headers, data=multi_form)
    res_json = response.json()
    return res_json


if __name__ == '__main__':
    wx_webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2823f309-1e7f-4178-b603-d0fa2f7e9c60"
    lark_webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/69d926ba-6790-40c3-822b-cdfb1e04c17e"
    content = "Hello, World!"
    image_path = r"D:\Desktop\签名\2.jpg"
    webhook_wx(wx_webhook_url, content, image_path=image_path)
    webhook_lark(lark_webhook_url, content, image_path=image_path)
    webhook_lark(lark_webhook_url, content)


