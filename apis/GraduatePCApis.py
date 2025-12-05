# coding: utf-8
import datetime
import json
import time

import pandas as pd
import requests
from utils.CookieUtils import trans_cookies
from utils.CommonUtils import generateGraduatepwdDefaultEncrypt
from utils.PassCaptcha import DetectCaptcha


# 河海大学研究生院
# http://yjss.hhu.edu.cn/home/stulogin
class HHUGraduatePCApis():
    def __init__(self):
        self.session = None
        self.author = 'cv-cat'
        self.detectCaptcha = DetectCaptcha()

    def getGraduateSession(self, username, password):
        self.username = username
        self.session = requests.session()
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7,ja;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        url = "https://yjss.hhu.edu.cn/student/default/index"
        response = self.session.get(url, headers=headers, verify=False, allow_redirects=False)
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7,ja;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        url = "https://yjss.hhu.edu.cn/home/stulogin"
        response = self.session.get(url, headers=headers, verify=False, allow_redirects=False)
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "http://yjss.hhu.edu.cn/student/default/index",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
        }
        url = "https://yjss.hhu.edu.cn/home/stulogin"
        response = self.session.get(url, headers=headers, verify=False)
        headers = {
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "http://yjss.hhu.edu.cn/home/stulogin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
        }
        url = "https://yjss.hhu.edu.cn/home/verificationcode"
        params = {
            "codetype": "stucode"
        }
        response = self.session.get(url, headers=headers, params=params, verify=False)
        imageContent = response.content
        captchaResult = self.detectCaptcha.detectImg(imageContent)
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "http://yjss.hhu.edu.cn",
            "Pragma": "no-cache",
            "Referer": "http://yjss.hhu.edu.cn/home/stulogin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
            "X-Requested-With": "XMLHttpRequest"
        }
        url = "https://yjss.hhu.edu.cn/home/stulogin_do"
        data = {
            "json": '{' + f'"UserId":"{username}","Password":"{password}","VeriCode":"{captchaResult}","url":"","city":""' + '}'
        }
        response = self.session.post(url, headers=headers, data=data, verify=False)
        res_text = response.text
        res_text = generateGraduatepwdDefaultEncrypt(res_text)


    def getAllLesson(self):
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "https://yjss.hhu.edu.cn/student/pygl/xscjcx",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        url = "http://yjss.hhu.edu.cn/student/pygl/xscjcx_list"
        params = {
            "_": str(int(time.time() * 1000))
        }
        response = self.session.get(url, headers=headers, params=params, verify=False)
        res_text = response.text
        res_text = generateGraduatepwdDefaultEncrypt(res_text)
        res_json = json.loads(res_text)
        # 保存pdf
        # url = "http://yjss.hhu.edu.cn/student/pygl/dcword_cj"
        # response = requests.post(url, headers=headers, cookies=cookies, verify=False)
        # res_content = response.content
        # with open('score.pdf', 'wb') as f:
        #     f.write(res_content)
        return res_json

    def post_jiangzuo(self):
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Origin': 'https://yjss.hhu.edu.cn',
            'Pragma': 'no-cache',
            'Referer': 'https://yjss.hhu.edu.cn/student/jdpy/sjrzjl',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        data = pd.read_excel(r"D:\Desktop\讲座内容.xlsx")
        data = data.to_numpy().tolist()
        for index, i in enumerate(data):
            data_json = {
                'id': '0',
                'jzdd': i[0],
                'zzdw': i[1],
                'jztm': i[2],
                'zcr': i[4],
                'jzsj': i[3].strftime('%Y-%m-%d'),
                'zynr': i[5],
                'xh': self.username,
            }
            data = {
                'json': json.dumps(data_json, ensure_ascii=False, separators=(',', ':'))
            }
            response = self.session.post('https://yjss.hhu.edu.cn/student/jdpy/py_jd_xsjzkh_edit', headers=headers, data=data)
            res_text = response.text
            res_text = generateGraduatepwdDefaultEncrypt(res_text)
            res_json = json.loads(res_text)

            if response.status_code >= 200 and response.status_code < 300:
                print(f"讲座 {i[2]} 提交成功")
            else:
                print(f"讲座 {i[2]} 提交失败: {res_json['message']}")
        return res_json
if __name__ == '__main__':
    username = '231607010123'
    password = 'github@cv-cat'
    hhuGraduatePCApis = HHUGraduatePCApis()
    hhuGraduatePCApis.getGraduateSession(username, password)
    # res_json = hhuGraduatePCApis.getAllLesson()
    # for i in res_json['xwklist']:
    #     print(i)
    # for i in res_json['fxwklist']:
    #     print(i)
    res_json = hhuGraduatePCApis.post_jiangzuo()
    print(res_json)
