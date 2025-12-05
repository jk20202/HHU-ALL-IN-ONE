import json
import re
import time
import requests
from utils.CommonUtils import generatePCpwdDefaultEncrypt, generateFingerPrint


# HHU官网 APIs
# https://authserver.hhu.edu.cn/authserver/login
class HHUPCApis():
    def __init__(self):
        self.author = 'cv-cat'

    def getPCSession(self, username, password):
        session = requests.Session()

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        url = "https://authserver.hhu.edu.cn/authserver/login"
        response = session.get(url, headers=headers)

        session.cookies.update({
            'org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE': 'zh_CN'
        })
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "https://authserver.hhu.edu.cn/authserver/login",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        url = "https://authserver.hhu.edu.cn/authserver/login"
        response = session.get(url, headers=headers)
        res_text = response.text
        execution = re.findall(r'type="hidden" name="execution" value="(.*?)"', res_text)[0]
        pwdDefaultEncryptSalt = re.findall(r'id="pwdEncryptSalt" value="(.*?)"', res_text)[0]
        finger_headers  = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "https://authserver.hhu.edu.cn/authserver/login",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        finger_url  = "https://authserver.hhu.edu.cn/authserver/bfp/info"
        bfp = generateFingerPrint()
        # bfp = '8BE1C74B906D1C47C7E41C9F4486728F'
        finger_params = {
            "bfp": bfp,
            "_": str(int(time.time() * 1000))
        }
        response = session.get(finger_url, headers=finger_headers, params=finger_params)
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://authserver.hhu.edu.cn",
            "Pragma": "no-cache",
            "Referer": "https://authserver.hhu.edu.cn/authserver/login",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        url = "https://authserver.hhu.edu.cn/authserver/login"
        pwdDefaultEncrypt = generatePCpwdDefaultEncrypt(password, pwdDefaultEncryptSalt)
        data = {
            "username": username,
            "password": pwdDefaultEncrypt,
            "captcha": "",
            "_eventId": "submit",
            "cllt": "userNameLogin",
            "dllt": "generalLogin",
            "lt": "",
            "execution": execution
        }
        response = session.post(url, headers=headers, data=data, allow_redirects=False)
        redirectUrl = response.headers["Location"]

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "https://authserver.hhu.edu.cn/authserver/login",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        response = session.get(redirectUrl, headers=headers, allow_redirects=False)
        redirectUrl = response.headers["Location"]
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "https://authserver.hhu.edu.cn/authserver/login",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        response = session.get(redirectUrl, headers=headers, allow_redirects=False)
        redirectUrl = response.headers["Location"]

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://authserver.hhu.edu.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        response = session.get(redirectUrl, headers=headers, verify=False, allow_redirects=False)
        redirectUrl = response.headers["Location"]
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        response = session.get(redirectUrl, headers=headers, allow_redirects=False)
        redirectUrl = response.headers["Location"]
        assert "authserver.hhu.edu.cn/personalInfo/personCenter/index.html" in redirectUrl, "重定向链接异常！"
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        response = session.get(redirectUrl, headers=headers, allow_redirects=False)
        redirectUrl = response.headers["Location"]
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        response = session.get(redirectUrl, headers=headers)
        #===
        headers = {
            "Host": "my.hhu.edu.cn",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Referer": response.url,
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

        url = "https://my.hhu.edu.cn/portal-web/guest/hhdx/index.html"
        params = {
            "t": str(int(time.time() * 1000))
        }
        response = session.get(url, headers=headers, params=params)
        refer = response.url
        res_text = response.text
        slide_splice = re.findall(r'data-callback="scanBox-img" data-url="(.*?)"', res_text)[0]
        heyw_rss_splice = re.findall(r'data-callback="heyw-rss-list" data-url="(.*?)"', res_text)[0]
        oa_rss_splice = re.findall(r'data-callback="OA-rss-list" data-url="(.*?)"', res_text)[0]

        headers = {
            "Host": "my.hhu.edu.cn",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": refer,
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        url = f"https://my.hhu.edu.cn{slide_splice}"
        params = {
            "t": str(int(time.time() * 1000))
        }
        response = session.get(url, headers=headers, params=params)

        headers = {
            "Host": "my.hhu.edu.cn",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": refer,
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

        url = f"https://my.hhu.edu.cn{heyw_rss_splice}"
        params = {
            "t": str(int(time.time() * 1000))
        }
        response = session.get(url, headers=headers, params=params)

        headers = {
            "Host": "my.hhu.edu.cn",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": refer,
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

        url = f"https://my.hhu.edu.cn{oa_rss_splice}"
        params = {
            "t": str(int(time.time() * 1000))
        }
        response = session.get(url, headers=headers, params=params)

        headers = {
            "Host": "my.hhu.edu.cn",
            "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Referer": refer,
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

        url = "https://my.hhu.edu.cn/portal-web/html/index.html"
        params = {
            "t": str(int(time.time() * 1000))
        }
        response = session.get(url, headers=headers, params=params, allow_redirects=False)
        redirectUrl = response.headers["Location"]

        headers = {
            "Host": "my.hhu.edu.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

        url = "https://my.hhu.edu.cn/portal-web/html/oauth2client/oauth2login"
        response = session.get(url, headers=headers, allow_redirects=False)
        redirectUrl = response.headers["Location"]

        headers = {
            "Host": "my.hhu.edu.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

        response = session.get(redirectUrl, headers=headers, allow_redirects=False)
        redirectUrl = response.headers["Location"]

        headers = {
            "Host": "authserver.hhu.edu.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

        response = session.get(redirectUrl, headers=headers, allow_redirects=False)
        redirectUrl = response.headers["Location"]

        headers = {
            "Host": "authserver.hhu.edu.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

        response = session.get(redirectUrl, headers=headers, allow_redirects=False)
        redirectUrl = response.headers["Location"]

        headers = {
            "Host": "my.hhu.edu.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        response = session.get(redirectUrl, headers=headers, allow_redirects=False)
        redirectUrl = response.headers["Location"]

        headers = {
            "Host": "my.hhu.edu.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

        response = session.get(redirectUrl, headers=headers, allow_redirects=False)
        redirectUrl = response.headers["Location"]

        headers = {
            "Host": "my.hhu.edu.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

        response = session.get(redirectUrl, headers=headers, allow_redirects=False)
        redirectUrl = response.headers["Location"]

        headers = {
            "Host": "my.hhu.edu.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

        response = session.get(redirectUrl, headers=headers, allow_redirects=False)
        redirectUrl = response.headers["Location"]

        headers = {
            "Host": "my.hhu.edu.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        response = session.get(redirectUrl, headers=headers)
        return session

    def getUserInfo(self, session):
        headers = {
            "Host": "my.hhu.edu.cn",
            "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://my.hhu.edu.cn/portal-web/html/index.html?t=1725617081400",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        url = "https://my.hhu.edu.cn/portal-web/api/proxy/interface/api/rest/v1/personalInterface/getUserInfo"
        params = {
            "t": str(int(time.time() * 1000)),
            "access_token": session.cookies["access_token"]
        }
        response = session.get(url, headers=headers, params=params)
        res_json = response.json()
        return res_json

if __name__ == '__main__':
    username = '231607010123'
    password = 'github@cv-cat'

    hhuPCApis = HHUPCApis()
    session = hhuPCApis.getPCSession(username, password)
    print(session)
    res = hhuPCApis.getUserInfo(session)
    print(json.dumps(res, ensure_ascii=False, indent=4))

