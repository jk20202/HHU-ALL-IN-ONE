from loguru import logger
from concurrent.futures import ThreadPoolExecutor
import re
import os
import json
import time

import yaml
import qrcode
import schedule
from apis.PCApis import HHUPCApis
from utils.CommonUtils import get_next_data
from utils.WebHookApis import webhook_wx, webhook_lark

current_project_directory = os.path.dirname(os.path.dirname(__file__))
log_name = os.path.join(current_project_directory, 'main.log')
logger.add(log_name, encoding="utf-8", enqueue=True, catch=True, rotation="10MB", retention="10 days", mode="a")

# HHU 羽毛球场地预约
# https://cggl.hhu.edu.cn//user/userBook/userBook.html#/resourceDetail?eventId=a63735d9fbe997c639b25f5f52723d8d&eventBookWay=2
class HHUAppointmentApis():
    def __init__(self, user_info):
        self.author = 'cv-cat'
        self.pcApi = HHUPCApis()
        self.appointment_success_order_number = 0
        self.is_appoint = False
        self.name = None
        self.chinese_name = None
        self.site_name = None
        self.session = None
        self.all_slot = None
        self.eventId = None
        self.book_date = None
        self.user_info = user_info
        self.message_queue = []

    def init_session(self, username, password):
        self.session = self.pcApi.getPCSession(username, password)
        user_info = self.pcApi.getUserInfo(self.session)
        user_info = user_info['data']['userInfo']
        self.chinese_name = user_info['NAME']
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
        response = self.session.get('https://cggl.hhu.edu.cn//user/userBook/userBook.html', headers=headers, allow_redirects=False)
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
        response = self.session.get(Location, headers=headers, allow_redirects=False)
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
        response = self.session.get(Location, headers=headers, allow_redirects=False)
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
        response = self.session.get(Location, headers=headers)

    def get_all_appointment_record(self):
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
            'eventName': '',
            'bookStatus': None,
            'startDate': '',
            'endDate': '',
            'pager': {
                'pageNum': 1,
                'pageSize': 10,
            },
        }
        response = self.session.post('https://cggl.hhu.edu.cn/api/v2/appBookGeneral/mine/list', headers=headers, json=json_data)
        res_json = response.json()
        return res_json

    def cancel_appointment(self, book_id):
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
            'id': book_id,
        }

        response = self.session.post('https://cggl.hhu.edu.cn/api/v2/appBookGeneral/mine/cancel', headers=headers, json=json_data)
        res_json = response.json()
        return res_json

    def cancel_some_appointment(self, save_site_name='羽毛球'):
        username = self.user_info['username']
        password = self.user_info['password']
        self.init_session(username, password)
        all_record = self.get_all_appointment_record()
        all_record = all_record['data']
        # 要删除的是 save_site_name 之外的预约 且 status 为 4 的预约
        record_to_cancel = list(filter(lambda x: x['status'] != 4 and save_site_name not in x['eventName'], all_record))
        for record in record_to_cancel:
            logger.info(f'正在取消 {self.name} {record["eventName"]} 的预约')
            cancel_res = self.cancel_appointment(record['id'])
            logger.info(f'取消结果 {json.dumps(cancel_res, ensure_ascii=False)}')

    def get_all_site(self):
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
        response = self.session.post('https://cggl.hhu.edu.cn/api/v2/appBookGeneral/event/list', headers=headers, json=json_data)
        res_json = response.json()
        return res_json


    def get_all_room(self, event_id, book_date):
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
        response = self.session.post('https://cggl.hhu.edu.cn/api/v2/appBookGeneral/date/slot/searchByDate', headers=headers, json=json_data)
        res_json = response.json()
        return res_json

    def appointment(self, event_id, book_date, bookSlotId, bookSlot, resourceId, slotOrder, scheduleId, resourceName):
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

        response = self.session.post('https://cggl.hhu.edu.cn/api/v2/appBookGeneral/book/afterConfirm', headers=headers, json=json_data)
        print(response.text)
        print(response)
        res_json = response.json()
        return res_json

    def quitTaskFlag(self):
        t = time.localtime()
        if t.tm_hour == 7 and t.tm_min == 1:
            return True

    def init_all_slot(self, site_name='江宁校区乒乓球馆'):
        self.site_name = site_name
        username = self.user_info['username']
        password = self.user_info['password']
        my_favorite_time = self.user_info['favorite_time_input']
        my_favorite_no = self.user_info['favorite_no_input']
        try:
            self.init_session(username, password)

        except Exception as e:
            logger.error(f'{self.name} 登录失败 {e}')
            return

        logger.info(f'正在为 {self.name} init {site_name} 的所有场地信息')

        all_site = self.get_all_site()
        # logger.info(f' {self.name} 所有的场馆信息 {json.dumps(all_site, ensure_ascii=False)}')
        badminton_site = list(filter(lambda x: site_name in x['name'], all_site['data']))[0]
        self.eventId = badminton_site['id']
        self.book_date = get_next_data()
        all_room = self.get_all_room(self.eventId, self.book_date)
        logger.info(f' {self.name} {site_name} 所有的场地信息 {json.dumps(all_room, ensure_ascii=False)}')
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
        all_slot = self.choice_favorite(all_slot, my_favorite_time, my_favorite_no)
        logger.info(f' {self.name} {site_name} 经过筛选后的时间段, {all_slot}')
        self.all_slot = all_slot

    def appoint_main(self, webhook_url=None, need_num=1):
        while not self.is_appoint or self.appointment_success_order_number < need_num:
            if self.quitTaskFlag():
                content = f'{self.name} 超时退出'
                logger.error(content)
                if webhook_url:
                    if 'wx_webhook_url' in webhook_url:
                        self.message_queue.append({
                            'send': webhook_wx,
                            'args': [webhook_url['wx_webhook_url'], content]
                        })
                        # webhook_wx(webhook_url['wx_webhook_url'], content)
                    if 'lark_webhook_url' in webhook_url:
                        self.message_queue.append({
                            'send': webhook_lark,
                            'args': [webhook_url['lark_webhook_url'], content]
                        })
                        # webhook_lark(webhook_url['lark_webhook_url'], content)
                logger.info(f'=============================================')
                return
            for slot in self.all_slot:
                resourceName = slot['resourceName']
                resourceId = slot['resourceId']
                logger.info(f'{self.name} 正在查看  {self.site_name} {resourceName} {self.book_date} 的 {slot["startTime"]}-{slot["endTime"]}')
                if slot['status'] == 0:
                    bookSlotId = slot['slotId']
                    scheduleId = slot['scheduleId']
                    bookSlot = f'{slot["startTime"]}-{slot["endTime"]}'
                    slotOrder = slot['slotOrder']
                    appointment_res = self.appointment(self.eventId, self.book_date, bookSlotId, bookSlot, resourceId, slotOrder, scheduleId, resourceName)
                    logger.info(f'11 {appointment_res}')
                    logger.info(f'{self.name}  {self.site_name} {resourceName} {self.book_date} 的 {slot["startTime"]}-{slot["endTime"]} 预约结果 {json.dumps(appointment_res, ensure_ascii=False)}')
                    if '最大预约次数' in appointment_res['message']:
                        content = f'{self.name} 预约失败  {self.site_name} {resourceName} {self.book_date} 的 {slot["startTime"]}-{slot["endTime"]}, {appointment_res["message"]}'
                        logger.error(content)
                        self.is_appoint = False
                        if webhook_url:
                            if 'wx_webhook_url' in webhook_url:
                                self.message_queue.append({
                                    'send': webhook_wx,
                                    'args': [webhook_url['wx_webhook_url'], content]
                                })
                                # webhook_wx(webhook_url['wx_webhook_url'], content)
                            if 'lark_webhook_url' in webhook_url:
                                self.message_queue.append({
                                    'send': webhook_lark,
                                    'args': [webhook_url['lark_webhook_url'], content]
                                })
                                # webhook_lark(webhook_url['lark_webhook_url'], content)
                        logger.info(f'=============================================')
                        return
                    if appointment_res['status'] == 0 and appointment_res['message'] == 'success':
                        book_id = appointment_res['extdata']['id']

                        qrcode_save_path = os.path.abspath(os.path.join(current_project_directory, 'static', 'qrcodes', f'qrcode {self.chinese_name} {self.site_name} {self.book_date}.png'))
                        self.generate_qrcode(book_id, qrcode_save_path)
                        content = f'{self.name} 预约成功 {self.site_name} {resourceName} {self.book_date} 的 {slot["startTime"]}-{slot["endTime"]}'
                        logger.info(content)
                        self.is_appoint = True
                        self.appointment_success_order_number += 1
                        if webhook_url:
                            if 'wx_webhook_url' in webhook_url:
                                self.message_queue.append({
                                    'send': webhook_wx,
                                    'args': [webhook_url['wx_webhook_url'], content, qrcode_save_path]
                                })
                                # webhook_wx(webhook_url['wx_webhook_url'], content)
                            if 'lark_webhook_url' in webhook_url:
                                self.message_queue.append({
                                    'send': webhook_lark,
                                    'args': [webhook_url['lark_webhook_url'], content, qrcode_save_path]
                                })
                                # webhook_lark(webhook_url['lark_webhook_url'], content)
                        logger.info(f'=============================================')
                        if self.is_appoint and self.appointment_success_order_number >= need_num:
                            return

    def choice_favorite(self, slotInfo, my_favorite_time, my_favorite_no):
        def sort_key(slot):
            startTime = slot['startTime']
            endTime = slot['endTime']
            start_minutes = int(startTime.split(':')[0]) * 60 + int(startTime.split(':')[1])
            end_minutes = int(endTime.split(':')[0]) * 60 + int(endTime.split(':')[1])
            resourceName = slot['resourceName']
            resourceNameNum = re.findall(r'\d+', resourceName)[0]
            time_priority = (float('inf'), float('inf'), float('inf'))
            no_priority = float('inf')
            if my_favorite_time:
                for time_index, time in enumerate(my_favorite_time):
                    time_minutes = int(time.split(':')[0]) * 60 + int(time.split(':')[1])
                    if start_minutes <= time_minutes <= end_minutes:
                        time_priority = (time_index, start_minutes, end_minutes)
                        break
            if my_favorite_no:
                for no_index, no in enumerate(my_favorite_no):
                    if str(no) == resourceNameNum:
                        no_priority = no_index
                        break
            return (no_priority, time_priority, -start_minutes)
        return sorted(slotInfo, key=sort_key)

    def get_order_detail(self, book_id):
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
            'bookMineId': book_id,
        }
        response = self.session.post('https://cggl.hhu.edu.cn/api/v2/appBookGeneral/mine/detail', headers=headers, json=json_data)
        res_json = response.json()
        return res_json

    def generate_sign(self, outerId):
        headers = {
            'Host': 'cggl.hhu.edu.cn',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c2d)XWEB/11581',
            'Content-Type': 'application/json',
            'Origin': 'https://cggl.hhu.edu.cn',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': f'https://cggl.hhu.edu.cn/wechat/book3/book.html?type=eventInfo?eventId={self.eventId}',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        json_data = {
            'outerId': outerId,
        }

        response = self.session.post('https://cggl.hhu.edu.cn/api/v2/appMobileSign/getSignCode', headers=headers, json=json_data)
        res_json = response.json()
        return res_json

    def generate_qrcode(self, book_id, save_path='qrcode.png'):
        order_detail = self.get_order_detail(book_id)
        outerId = order_detail['data']['resRecords'][0]['detailIds'][0]
        sign_res = self.generate_sign(outerId)['data']
        qrcode_str = f'https://cggl.hhu.edu.cn/wechat/book3/book.html#/shareSign/scan?qrCode={sign_res}&bookMineId={book_id}&outerId={outerId}'
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qrcode_str)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(save_path)


    def handle_message_queue(self):
        while self.message_queue:
            message = self.message_queue.pop(0)
            message['send'](*message['args'])
            time.sleep(4)

def load_env():
    project_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    env_path = os.path.abspath(os.path.join(project_path, 'env.yaml'))
    config = yaml.safe_load(open(env_path, 'r', encoding='utf-8'))
    config = config['HHU']['Appointment']
    return config

def main_step1(hhu_users, site_name, run_thread=False):
    if run_thread:
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(lambda user: user.init_all_slot(site_name), hhu_users)
    else:
        for user in hhu_users:
            user.init_all_slot(site_name)

def main_step2(hhu_users, webhook_url=None, run_thread=False, need_num=1):
    if run_thread:
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(lambda user: user.appoint_main(webhook_url, need_num), hhu_users)
    else:
        for user in hhu_users:
            user.appoint_main(webhook_url, need_num)

def main_step3(hhu_users):
    for user in hhu_users:
        user.handle_message_queue()

if __name__ == '__main__':
    # config = load_env()
    # users, site_name, run_thread, webhook_url = config['users'], config['site_name'], config['run_thread'], config['webhook_url']

    users = [
        {
            'username': '231607010123',
            'password': 'github@cv-cat',
            'favorite_time_input': ['15:00', '16:00', '17:00'],
            'favorite_no_input': ['1', '2'],
        },
        # {
        #     'username': '231607010025',
        #     'password': 'GA,418,520.',
        #     'favorite_time_input': ['14:00', '15:00', '16:00'],
        #     'favorite_no_input': ['3', '4'],
        # },
        # {
        #     'username': '231607010121',
        #     'password': 'Zzy20010721',
        #     'favorite_time_input': ['19:00', '20:00'],
        #     'favorite_no_input': ['5', '6'],
        # },
    ]

    site_name = '江宁校区羽毛球'
    # site_name = '江宁校区乒乓球'
    run_thread = True
    need_num = 3
    webhook_url = {
        "wx_webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2823f309-1e7f-4178-b603-d0fa2f7e9c60",
        "lark_webhook_url":  "https://open.feishu.cn/open-apis/bot/v2/hook/69d926ba-6790-40c3-822b-cdfb1e04c17e"
    }
    webhook_url = None
    hhu_users = []
    for user in users:
        hhu_user = HHUAppointmentApis(user)
        hhu_users.append(hhu_user)
        # logger.info(f'删除所有除了 {site_name} 的预约')
        # hhu_user.cancel_some_appointment('羽毛球')

    main_step1(hhu_users, site_name, run_thread)
    main_step2(hhu_users, webhook_url, run_thread, need_num)
    main_step3(hhu_users)

    # schedule.every().day.at("06:59").do(main_step1, hhu_users, site_name, run_thread)
    # schedule.every().day.at("07:00").do(main_step2, hhu_users, webhook_url, run_thread, need_num)
    # schedule.every().day.at("07:01").do(main_step3, hhu_users)
    # logger.info('开始定时任务')
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

