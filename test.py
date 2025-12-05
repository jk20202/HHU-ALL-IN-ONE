import requests


headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://authserver.hhu.edu.cn",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
url = "http://authserver.hhu.edu.cn/authserver/login"
params = {
    "service": "https://authserver.hhu.edu.cn/personalInfo/personCenter/index.html"
}
response = requests.get(url, headers=headers, params=params, verify=False, allow_redirects=False)

print(response.text)
print(response)
print(response.headers)