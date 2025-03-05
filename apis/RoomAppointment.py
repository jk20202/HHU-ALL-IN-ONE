import os.path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import json
from loguru import logger
import re
import time
import requests
import yaml

import schedule
from utils.CommonUtils import generatePCpwdDefaultEncrypt, get_current_data, get_next_data
from apis.PCApis import HHUPCApis
# HHU 羽毛球场地预约
# https://cggl.hhu.edu.cn//user/userBook/userBook.html#/resourceDetail?eventId=a63735d9fbe997c639b25f5f52723d8d&eventBookWay=2
class HHUAppointmentApis():
    def __init__(self):
        self.author = 'cv-cat'
        self.pcApi = HHUPCApis()
        self.name = None

    def init(self, session):
        user_info = self.pcApi.getUserInfo(session)
        user_info = user_info['data']['userInfo']
        self.name = f'{user_info["DEPARTNAME"]} 的 {user_info["ROLENAME"]} {user_info["NAME"]}'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Referer': 'https://my.hhu.edu.cn/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        response = session.get('https://cggl.hhu.edu.cn//user/userBook/userBook.html', headers=headers, allow_redirects=False)
        Location = response.headers['Location']
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Referer': 'https://my.hhu.edu.cn/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        response = session.get(Location, headers=headers, allow_redirects=False)
        Location = response.headers['Location']
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Referer': 'https://my.hhu.edu.cn/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        response = session.get(Location, headers=headers, allow_redirects=False)
        Location = response.headers['Location']
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Referer': 'https://my.hhu.edu.cn/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        response = session.get(Location, headers=headers)

    def get_all_site(self, session):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://cggl.hhu.edu.cn',
            'Pragma': 'no-cache',
            'Referer': 'https://cggl.hhu.edu.cn//user/userBook/userBook.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        json_data = {
            'fuzzy': '',
            'pager': {
                'pageNum': 1,
                'pageSize': 12,
            },
        }
        response = session.post('https://cggl.hhu.edu.cn/api/v2/appBookGeneral/event/list', headers=headers, json=json_data)
        res_json = response.json()
        return res_json


    def get_all_room(self, session, event_id, book_date):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://cggl.hhu.edu.cn',
            'Pragma': 'no-cache',
            'Referer': 'https://cggl.hhu.edu.cn//user/userBook/userBook.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        json_data = {
            'date': book_date,
            'eventId': event_id,
        }
        response = session.post('https://cggl.hhu.edu.cn/api/v2/appBookGeneral/date/slot/searchByDate', headers=headers, json=json_data)
        res_json = response.json()
        return res_json

    def appointment(self, session, event_id, book_date, bookSlotId, bookSlot, resourceId, slotOrder, scheduleId, resourceName):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://cggl.hhu.edu.cn',
            'Pragma': 'no-cache',
            'Referer': 'https://cggl.hhu.edu.cn//user/userBook/userBook.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        json_data = {
            'eventId': event_id,
            'extAttr': '',
            'payAmount': 0,
            'records': [
                {
                    'bookDate': book_date,
                    'bookSlotId': bookSlotId,
                    'bookSlot': bookSlot,
                    'number': 1,
                    'price': '',
                    'resourceId': resourceId,
                    'slotOrder': slotOrder,
                    'seatId': '',
                    'scheduleId': scheduleId,
                    'resourceName': resourceName
                },
            ],
        }

        response = session.post('https://cggl.hhu.edu.cn/api/v2/appBookGeneral/book/afterConfirm', headers=headers, json=json_data)
        res_json = response.json()
        return res_json

    def appoint_main(self, username, password, site_name='江宁校区乒乓球馆', my_favorite_time=None, my_favorite_no=None):
        try:
            session = self.pcApi.getPCSession(username, password)
        except Exception as e:
            logger.error(f'{self.name} 登录失败 {e}')
            return
        self.init(session)
        logger.info(f'正在为 {self.name} 预约 {site_name}')
        all_site = self.get_all_site(session)
        logger.info(f'所有的场馆信息')
        logger.info(json.dumps(all_site, ensure_ascii=False))
        badminton_site = list(filter(lambda x: site_name in x['name'], all_site['data']))[0]
        eventId = badminton_site['id']
        book_date = get_next_data()
        all_room = self.get_all_room(session, eventId, book_date)
        logger.info(f'{site_name} 所有的场地信息')
        logger.info(json.dumps(all_room, ensure_ascii=False))
        all_room = all_room['data']['list']
        all_slot = []
        for room in all_room:
            resourceName = room['name']
            resourceId = room['id']
            slotInfo = room['slotInfo'] if room['slotInfo'] else []
            for slot in slotInfo:
                slot['resourceName'] = resourceName
                slot['resourceId'] = resourceId
                all_slot.append(slot)
        all_slot = list(filter(lambda x: x['status'] == 0, all_slot))
        logger.info(f'{site_name} 所有的可预约时间段')
        all_slot = self.choice_favorite(all_slot, my_favorite_time, my_favorite_no)
        logger.info(f'经过筛选后的时间段, {all_slot}')
        for slot in all_slot:
            resourceName = slot['resourceName']
            resourceId = slot['resourceId']
            logger.info(f'正在查看 {resourceName} 的 {slot["startTime"]}-{slot["endTime"]}')
            if slot['status'] == 0:
                bookSlotId = slot['slotId']
                scheduleId = slot['scheduleId']
                bookSlot = f'{slot["startTime"]}-{slot["endTime"]}'
                slotOrder = slot['slotOrder']
                appointment_res = self.appointment(session, eventId, book_date, bookSlotId, bookSlot, resourceId, slotOrder, scheduleId, resourceName)
                logger.info(json.dumps(appointment_res, ensure_ascii=False))
                if '最大预约次数' in appointment_res['message']:
                    logger.error(f'{self.name} 预约失败 {resourceName} 的 {slot["startTime"]}-{slot["endTime"]}, {appointment_res["message"]}')
                    break
                if appointment_res['status'] == 0 and appointment_res['message'] == 'success':
                    logger.info(f'{self.name} 预约成功 {resourceName} 的 {slot["startTime"]}-{slot["endTime"]}')
                    break
        logger.info(f'=============================================')

    def choice_favorite(self, slotInfo, my_favorite_time, my_favorite_no):
        def sort_key(slot):
            startTime = slot['startTime']
            endTime = slot['endTime']
            start_minutes = int(startTime.split(':')[0]) * 60 + int(startTime.split(':')[1])
            end_minutes = int(endTime.split(':')[0]) * 60 + int(endTime.split(':')[1])
            resourceName = slot['resourceName']
            resourceNameNum = re.findall(r'\d+', resourceName)[0]
            time_priority = float('inf')
            no_priority = float('inf')
            if my_favorite_time:
                for time_index, time in enumerate(my_favorite_time):
                    time_minutes = int(time.split(':')[0]) * 60 + int(time.split(':')[1])
                    if start_minutes <= time_minutes <= end_minutes:
                        time_priority = time_index
                        break
            if my_favorite_no:
                for no_index, no in enumerate(my_favorite_no):
                    if str(no) == resourceNameNum:
                        no_priority = no_index
                        break
            return (time_priority, no_priority, -start_minutes)
        return sorted(slotInfo, key=sort_key)

def load_env():
    project_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    env_path = os.path.abspath(os.path.join(project_path, 'env.yaml'))
    config = yaml.safe_load(open(env_path, 'r', encoding='utf-8'))
    config = config['HHU']['Appointment']
    return config


def main(users, site_name, my_favorite_time_input, my_favorite_no_input, run_thread=False):
    if run_thread:
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(lambda user: HHUAppointmentApis().appoint_main(user['username'], user['password'], site_name, my_favorite_time_input, my_favorite_no_input), users)
    else:
        for user in users:
            hhuAppointmentApis = HHUAppointmentApis()
            username = user['username']
            password = user['password']
            hhuAppointmentApis.appoint_main(username, password, site_name, my_favorite_time_input, my_favorite_no_input)



if __name__ == '__main__':
    # config = load_env()
    # users, site_name, my_favorite_time_input, my_favorite_no_input, run_thread = config['users'], config['site_name'], config['my_favorite_time_input'], config['my_favorite_no_input'], config['run_thread']
    users = [
        {
            'username': '231607010123',
            'password': 'github/cv-cat',
        }
    ]
    my_favorite_time_input = [
        '18:00',
        '19:00'
    ]
    my_favorite_no_input = [
        '11',
        '9'
    ]
    site_name = '江宁校区羽毛球馆'
    run_thread = True

    # main(users, site_name, my_favorite_time_input, my_favorite_no_input, run_thread)

    schedule.every().day.at("07:00").do(main, users, site_name, my_favorite_time_input, my_favorite_no_input)
    while True:
        schedule.run_pending()
        time.sleep(1)


