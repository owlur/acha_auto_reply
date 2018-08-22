import requests
import time
import pymongo
from bson.objectid import ObjectId

base_url = 'http://api.acha.io:3000/user'
API_KEY = '33233C0EB2C9CA56566FD7D503F100ABDBE012306B4EB812C3C9E83129E8495D'
user_name = 'acha'
password = 'achasoma09!!'
conn = pymongo.MongoClient('mongodb://%s:%s@127.0.0.1' % (user_name, password))
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

        if res['result'] == 'success':
            reserv_list = res['reservList']
            for reserv in reserv_list:
                reserv['reservTime'] = time.strptime(reserv['reservTime'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
            print('예약 리스트 : ', res['reservList'])

            return res['reservList']
        elif res['result'] == 'failed':
            print(res)
            #error_code = res['msg'].split(' : ')[1]
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
    params = {'key' : API_KEY, 'kakaoUserKey' : user_key, 'reservToken': token, 'reservName': person_name,\
              'reservNumber': int(person_number)}
    print('match send data : ')
    print(params)
    res = requests.get(base_url + '/reserv/match', params)
    return res.json()


def get_reservation(reservation_id):
    pass


def get_reserv_local(start, end):
    res = reserv_collection.find({'reservTime': {'$gte': start, '$lte': end}}, {'storeId': 1, 'phoneNumber': 1, \
                                                                           'reservTime': 1})
    for i in res:
        print(i)

    return res


def get_alarm_interval():
    pass