import requests
import time
import pymongo
from datetime import datetime, timedelta
from collections import deque

base_url = 'http://api.acha.io:3000/user'
API_KEY = '33233C0EB2C9CA56566FD7D503F100ABDBE012306B4EB812C3C9E83129E8495D'
user_name = 'acha'
password = 'achasoma09!!'
conn = pymongo.MongoClient('mongodb://%s:%s@127.0.0.1:27017/acha' % (user_name, password))
acha_db = conn.get_database('acha')
reserv_collection = acha_db.get_collection('Reserv')
store_collection = acha_db.get_collection('Store')


def get_reservation_list(user_key='', phone_number=''):
    if user_key or phone_number:
        params = {'key': API_KEY, 'kakaoUserKey': user_key, 'phoneNumber': phone_number, 'status': 'reserved'}
        res = requests.get(base_url + '/reserv/search', params)
        if res.status_code != 200:
            return False
        res = res.json()
        res = res['reserv'].extend(res['store']).copy()

        if res['result'] == 'success':
            reserv_list = res['reservList']
            for reserv in reserv_list:
                reserv['reservTime'] = time.strptime(reserv['reservTime'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
            print('예약 리스트 : ', res['reservList'])

            return res['reservList']
        elif res['result'] == 'failed':
            print(res)
            # error_code = res['msg'].split(' : ')[1]
            return []
        else:
            return False
    else:
        return False


def check_regist(user_key):
    params = {'key': API_KEY, 'kakaoUserKey': user_key}
    res = requests.get(base_url + '/info/regCheck', params)
    if res.status_code != 200:
        return False

    res = res.json()
    print('유저등록 확인:', res)
    if res['isReg']:
        return 'true'
    else:
        return 'false'


def user_regist(user_key, phone_number):
    try:
        params = {'key': API_KEY, 'kakaoUserKey': user_key, 'phoneNumber': phone_number}
        res = requests.get(base_url + '/info/reg', params)
        print('유저등록', res.json())
        return True
    except:
        return False


def reservation_cancel(user_key, reservation_id):
    res = reserv_status_edit(user_key, reservation_id, 'usercancel')
    return res.json()


def reservation_confirm(user_key, reservation_id):
    res = reserv_status_edit(user_key, reservation_id, 'reserved')
    return res.json()


def reserv_status_edit(user_key, reservation_id, status):
    params = {'key': API_KEY, 'kakaoUserKey': user_key, 'reservId': reservation_id, 'status': status}
    res = requests.get(base_url + '/reserv/edit', params)
    return res


def reserv_match(user_key, token, person_name, person_number):
    params = {'key': API_KEY, 'kakaoUserKey': user_key, 'reservToken': token, 'reservName': person_name, \
              'reservNumber': int(person_number)}
    print('match send data : ')
    print(params)
    res = requests.get(base_url + '/reserv/match', params)
    return res.json()


def get_reservation(reservation_id):
    pass


def get_reserv_local(start, end):
    """
    :param start: datetime.datetime object
    :param end: datetime.datetime object
    :return:
    """
    res = reserv_collection.find({'reservTime': {'$gte': start, \
                                                 '$lte': end}, \
                                  'currentStatus': 'reserved'},
                                 {'storeId': 1, 'phoneNumber': 1, 'reservTime': 1, 'name': 1, 'reservNumber': 1, \
                                  'reservToken': 1})
    return res


def get_store_info(object_id):
    res = store_collection.find_one({'_id': object_id}, {'alarmInterval': 1, 'address': 1, 'storeName': 1})
    return res


def get_today_alrim_list():
    """
    새벽 3시 실행
    당일 새벽 4시 ~ 다음날 새벽 4시에 전송해야할 알림 리스트
    :return:
    """
    now = datetime.now()
    start = now.replace(hour=4, minute=0, second=0, microsecond=0)
    week_end = start + timedelta(7)
    seven_day_reserv = get_reserv_local(start, week_end)
    today_end = start + timedelta(1)

    stores = {}
    res = []
    for reserv in seven_day_reserv:
        #reserv['reservTime'] = datetime.strptime(reserv['reservTime'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
        if reserv['storeId'] not in stores:
            store_info = get_store_info(reserv['storeId'])
            stores[reserv['storeId']] = {'alarm_interval': store_info.get('alarmInterval'),
                                         'store_name': store_info['storeName'],
                                         'address': store_info['address']}

        store_info = stores[reserv['storeId']]

        if not store_info['alarm_interval']:
            continue

        for alarm_interval in store_info['alarm_interval']:
            alarm_interval = int(alarm_interval)
            send_time = reserv['reservTime'] - timedelta(minutes=alarm_interval)
            if send_time < today_end:
                res.append({'token': reserv['reservToken'],
                            'store_name': store_info['store_name'],
                            'person_name': reserv['name'],
                            'reserv_date': reserv['reservTime'],
                            'person_num': reserv['reservNumber'],
                            'until_time': alarm_interval,
                            'address': store_info['address'],
                            'phone_number': reserv['phoneNumber'],
                            'send_time': send_time})

    return deque(sorted(res, key=lambda x: x['send_time']))
