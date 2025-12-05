import json

import requests

cookies = {
    'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0dCI6ImNhcyIsImV4cCI6MTc3MjYyNTk5MSwibm93IjoxNzQxMDg5OTkxLCJ0IjoiMjMxNjA3MDEwMTIzIn0.e3wUie3b0ZhcnE7hrlOFdKTz9QEd6MmM9k6-9FoFxxI',
    'ASP.NET_SessionId': 'gfpe15k2icjgbdjzzrrhi0bx',
    '__LOGINCOOKIE__': '',
    '__SINDEXCOOKIE__': 'eb8ce962a0ca4db7ff89fc87d30c5601',
}

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
    # 'Cookie': 'token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0dCI6ImNhcyIsImV4cCI6MTc3MjYyNTk5MSwibm93IjoxNzQxMDg5OTkxLCJ0IjoiMjMxNjA3MDEwMTIzIn0.e3wUie3b0ZhcnE7hrlOFdKTz9QEd6MmM9k6-9FoFxxI; ASP.NET_SessionId=gfpe15k2icjgbdjzzrrhi0bx; __LOGINCOOKIE__=; __SINDEXCOOKIE__=eb8ce962a0ca4db7ff89fc87d30c5601',
}

data = {
    'json': '{"id":"0","jzdd":"南京中禹研究院实践基地","zzdw":"南京中禹研究院实践基地","jztm":"迎新讲座--走进中禹研究院","zcr":"缪雅洁","jzsj":"2024-07-15","zynr":"介绍了基地单位的基本情况，包括单位主要业务方向、核心技术与产品、重点项目案例；单位组织架构、团队情况、导师介绍等。","xh":"231607010123"}',
}

# response = requests.post('https://yjss.hhu.edu.cn/student/jdpy/py_jd_xsjzkh_edit', cookies=cookies, headers=headers, data=data)
# print(response.text)

print(json.loads(data['json']))

import numpy as np
from numpy import ndarray

a = [np.array(['2', 2]), np.array([3, 4])]
c = np.array(a, dtype=ndarray)
print(c)