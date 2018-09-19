import requests
import utils

alrim_api_base_url = 'https://api-alimtalk.cloud.toast.com'
app_key ='OrJbsCa3geKuuqv8'
secret = 'Ycdr64tw'

header = {'X-Secret-Key': secret, 'Content-Type': 'application/json;charset=UTF-8'}

plusFriendId = 'ah_cha'


def send_interval_alrim(phone_number, store_name, person_name, person_num, date, until_date, address, token):
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
                          '남은일수': until_date, 'mobile_url': 'api.acha.io:3000/user/map?addr=%s' % address, \
                          'pc_url': 'api.acha.io:3000/user/map?addr=%s' % address}
    return send_alrim(template_code, phone_number, template_parameter)


def send_feedback_alrim(phone_number, store_name, person_name, token):
    template_coed = 'SRM0003'
    template_parameter = {'상호명': store_name, '이름': person_name, '시간': '어제', '소요시간': '2분', '예약번호': token }
    pass


def send_alrim(template_code, phone_number, template_parameter):
    params = {
        "plusFriendId": plusFriendId,
        "templateCode": template_code,
        "recipientList": [{
            "recipientNo": phone_number,
            "templateParameter": template_parameter
        }]
    }

    res = requests.post(alrim_api_base_url + '/alimtalk/v1.0/appkeys/' + app_key + '/messages', json=params,
                        headers=header)
    return res.json()


def get_alrim_status(request_id):
    params = {
        'requestId' : request_id
    }
    res = requests.get(alrim_api_base_url + 'slimtalk/v1.1/appkeys/' + app_key + '/messages', params=params,
                          headers=header).json()

    return res['messageSearchResultResponse']['messages']