import requests
import utils
from datetime import datetime
import re

alrim_api_base_url = 'https://api-alimtalk.cloud.toast.com'
alrim_api_app_key = 'OrJbsCa3geKuuqv8'
secret = 'Ycdr64tw'

sms_api_base_url = 'https://api-sms.cloud.toast.com'
sms_api_app_key = 'm7g6BVXzT1UEulm3'

alrim_header = {'X-Secret-Key': secret, 'Content-Type': 'application/json;charset=UTF-8'}
sms_header = {'Content-Type': 'application/json;charset=UTF-8'}

if utils.is_test():
    plus_friend_id = 'ah_cha'
else:
    plus_friend_id = 'acha'


def send_interval_alrim(phone_number, store_name, person_name, person_num, date, until_date, road_address, detail_address, token):
    date = utils.datetime2str(date)
    until_date = int(until_date)
    if until_date >= 1440:
        template_code = 'RRM0004'
        until_date = '%d일' % (until_date // 1440)
    else:
        template_code = 'RRM0003'
        if until_date >= 60:
            if until_date % 60 == 0:
                until_date = '%d시간' % (until_date // 60)
            else:
                until_date = '%d시간 %d분' % (until_date // 60, until_date % 60)
        else:
            until_date = '%d분' % until_date

    template_parameter = {'상호명': store_name, '이름': person_name, '인원': person_num, '날짜': date, '예약번호': token, \
                          '남은일수': until_date, \
                          'mobile_url': 'api.acha.io:3000/user/map?addr=%s&storeName=%s&detailAddress=%s' % (road_address, store_name, detail_address), \
                          'pc_url': 'api.acha.io:3000/user/map?addr=%s&storeName=%s&detailAddress=%s' % (road_address, store_name, detail_address)}
    return send_alrim(template_code, phone_number, template_parameter)


def send_feedback_alrim(phone_number, store_name, person_name, token):
    template_coed = 'SRM0003'
    template_parameter = {'상호명': store_name, '이름': person_name, '시간': '어제', '소요시간': '2분', '예약번호': token }
    pass


def send_store_cancel(phone_number, store_name, persone_name, person_num, date, store_phone_num, content):
    template_code = 'SCR0001'
    date = datetime.strptime(date.split('.')[0], '%Y-%m-%dT%H:%M:%S')
    date =utils.datetime2str(date)
    # 매장 번호에 하이픈(-) 추가
    store_phone_num = re.sub(r'(^02.{0}|^01.{1}|[0-9]{3})([0-9]+)([0-9]{4})', r'\1-\2-\3', store_phone_num)
    template_parameter = {'상호명': store_name,
                          '이름': persone_name,
                          '인원': person_num,
                          '날짜': date,
                          '매장연락처': store_phone_num,
                          '취소사유': content}
    return send_alrim(template_code, phone_number, template_parameter)


def send_alrim(template_code, phone_number, template_parameter):
    params = {
        "plusFriendId": plus_friend_id,
        "templateCode": template_code,
        "recipientList": [{
            "recipientNo": phone_number,
            "templateParameter": template_parameter
        }]
    }

    res = requests.post(alrim_api_base_url + '/alimtalk/v1.0/appkeys/' + alrim_api_app_key + '/messages', json=params,
                        headers=alrim_header)
    return res.json()


def get_alrim_status(request_id):
    params = {
        'requestId' : request_id
    }
    res = requests.get(alrim_api_base_url + '/alimtalk/v1.1/appkeys/' + alrim_api_app_key + '/messages', params=params,
                       headers=alrim_header).json()

    return res['messageSearchResultResponse']['messages'][0]


def send_sms(sender_no, recipent_no, content):
    params = {
        'body': content,
        'sendNo': sender_no,
        'recipientList':[{
          'recipientNo': recipent_no
        }]
    }
    res = requests.post(sms_api_base_url + '/sms/v2.1/appKeys/' + sms_api_app_key + '/sender/sms', json=params, headers=sms_header)

    return res