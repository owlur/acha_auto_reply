"""
시간 값을 가져올 때 주의할점
 - mongodb는 기본적으로 UTC시간으로 저장한다
 - 따라서 시간을 가져오거나 조회할 떄는 반드시 +9시간/-9시간을 해서 한국시간에 맞춰줘야한다
"""
import requests
import pymongo
from datetime import datetime, timedelta
from collections import deque
import utils
import pymysql
import secret_setting

if utils.is_test():
    print('start test mode')
    base_url = 'http://test.acha.io:3000/user'
else:
    base_url = 'http://api.acha.io:3000/user'

API_KEY = secret_setting.SERVER_API_KEY

def local_initilize():
    user_name = secret_setting.DB_USER
    password = secret_setting.DB_PASSWORD
    global feedback_collection
    conn = pymongo.MongoClient('mongodb://%s:%s@127.0.0.1:27017/acha' % (user_name, password))
    acha_db = conn.get_database('acha')
    #reserv_collection = acha_db.get_collection('Reserv')
    #store_collection = acha_db.get_collection('Store')
    feedback_collection = acha_db.get_collection('Feedback')


def save_feedback(token, question_list, answer_list):
    print(question_list, answer_list)
    store_id, user_id = get_store_user_id_by_token_mysql(token)
    update_dict = {'storeID': store_id}
    update_dict.update({question: answer for question, answer in zip(question_list, answer_list)})
    print(update_dict)
    res = feedback_collection.update_one({'userUUID': user_id}, {'$push': {'feedbacks': update_dict}}, upsert=True)
    return res


def mysql_initailize():
    user = 'acha'
    passwd = 'acha09!!'
    global conn
    conn = pymysql.connect(host='127.0.0.1', port=3306, user=user, password=passwd, db='acha', charset='utf8')
    global cur
    cur = conn.cursor(pymysql.cursors.DictCursor)


def query_mysql(query):
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(query)
    res = cur.fetchall()
    cur.close()
    return res

# def get_reserv_local(start, end, status, **kwargs):
#     """
#     :param start: datetime.datetime object
#     :param end: datetime.datetime object
#     :return:
#     """
#     if kwargs:
#         res = reserv_collection.find({'reservTime': {'$gte': start, '$lte': end}, 'currentStatus': status}, kwargs)
#     else:
#         res = reserv_collection.find({'reservTime': {'$gte': start, '$lte': end}, 'currentStatus': status},
#                                  {'storeId': 1, 'phoneNumber': 1, 'reservTime': 1, 'name': 1, 'reservNumber': 1, \
#                                   'reservToken': 1})
#     return res


def get_store_info_mysql(store_id, columns=None):
    if not columns:
        columns = ['firstAlarm', 'secondAlarm', 'storeName', 'fullAddress', 'roadAddress', 'detailAddress']

    query = 'SELECT %s FROM StoreLJoinAlarm WHERE storeUUID = "%s"' % (','.join(columns), store_id)
    #print(query)
    res = query_mysql(query)
    #print(res)
    return res[0]


def get_reserv_mysql(start, end, status, columns=None):
    if not columns:
        columns = ['storeUUID', 'userPhoneNumber', 'reservTime', 'reservName', 'reservNumber', 'reservToken']

    start = start.strftime('%Y-%m-%d %H:%M:%S')
    end = end.strftime('%Y-%m-%d %H:%M:%S')

    query = 'SELECT %s FROM ReservJoinStoreUser WHERE (reservTime >= "%s" and reservTime <= "%s") and reservStatus = "%s"' \
                      % (','.join(columns), start, end, status)

    res = query_mysql(query)
    #print(query)
    #print(res)
    return res


def get_store_user_id_by_token_mysql(token):
    query = 'SELECT storeUUID, userUUID FROM ReservJoinStoreUser WHERE reservToken = %s' % token

    res = query_mysql(query)
    print(res)

    return res[0]['storeUUID'], res[0]['userUUID']


# def get_store_info(object_id, **kwargs):
#     if kwargs:
#         res = store_collection.find_one({'_id': object_id}, kwargs)
#     else:
#         res = store_collection.find_one({'_id': object_id}, {'alarmInterval': 1, 'address': 1, 'storeName': 1})
#     return res


def get_feedback_list(start, minute=10):
    """
    10분 뒤의 알람 획득
    :return:
    """
    start -= timedelta(hours=24) # 24(1day) + 9(UTC)

    # start = now.replace(hour=4, minute=0, second=0, microsecond=0) if now.hour < 4 else now
    end = start + timedelta(minutes=minute)
    #reserv_list = get_reserv_local(start, end, 'visit', {'storeId': 1, 'phoneNumber': 1, 'reservTime': 1, 'name': 1, \
    #                                                     'reservToken': 1})

    reserv_list = get_reserv_mysql(start, end, 'visit', ['storeUUID', 'storePhoneNumber', 'reservTime', 'reservName', 'reservToken'])

    stores = {}
    res = []
    for reserv in reserv_list:
        # reserv['reservTime'] = datetime.strptime(reserv['reservTime'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
        if reserv['storeUUID'] not in stores:
            store_info = get_store_info_mysql(reserv['storeUUID'])
            get_store_info_mysql(reserv['storeUUID'])
            stores[reserv['storeUUID']] = {'store_name': store_info['storeName']}

        store_info = stores[reserv['storeUUID']]

        res.append({'token': reserv['reservToken'],
                    'store_name': store_info['store_name'],
                    'person_name': reserv['name'],
                    'phone_number': reserv['phoneNumber'],
                    'send_time': reserv['reservTime'] + timedelta(hours=24)})# + timedelta(hours=33)}) # 24(1day) + 9(UTC)

    return deque(sorted(res, key=lambda x: x['send_time']))


def get_alrim_list(start, minute=10):
    """
    10분 뒤의 알람 획득
    :return:
    """
    #start = datetime.utcnow()
    #start -= timedelta(hours=9)

    # start = now.replace(hour=4, minute=0, second=0, microsecond=0) if now.hour < 4 else now
    week_end = start + timedelta(7)
    #seven_day_reserv = get_reserv_local(start, week_end, 'reserved')
    seven_day_reserv = get_reserv_mysql(start, week_end, 'reserved')

    end_time = start + timedelta(minutes=minute)

    stores = {}
    res = []
    for reserv in seven_day_reserv:
        #print(reserv)
        # reserv['reservTime'] = datetime.strptime(reserv['reservTime'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
        if reserv['storeUUID'] not in stores:
            #store_info = get_store_info(reserv['storeId'])
            store_info = get_store_info_mysql(reserv['storeUUID'])
            stores[reserv['storeUUID']] = {'alarm_interval': (store_info['firstAlarm'], store_info['secondAlarm']), #'alarm_interval': store_info.get('alarmInterval'),
                                         'store_name': store_info['storeName'],
                                         'road_address': store_info['roadAddress'],
                                         'detail_address': store_info['detailAddress'],
                                         'full_address': store_info['fullAddress']}

        #store_info = stores[reserv['storeId']]
        store_info = stores[reserv['storeUUID']]
        #print(reserv)
        if not list(filter(lambda x:x, store_info['alarm_interval'])):
            continue

        for alarm_interval in store_info['alarm_interval']:
            alarm_interval = int(alarm_interval)
            send_time = reserv['reservTime'] - timedelta(minutes=alarm_interval)
            if send_time < end_time:
                res.append({'token': reserv['reservToken'],
                            'store_name': store_info['store_name'],
                            'person_name': reserv['reservName'], #reserv['name'],
                            'reserv_date': reserv['reservTime'], # + timedelta(hours=9),
                            'person_num': reserv['reservNumber'],
                            'until_time': alarm_interval,
                            'road_address': store_info['road_address'],
                            'detail_addresss': store_info['detail_address'],
                            'address': store_info['full_address'],
                            'phone_number': reserv['userPhoneNumber'],
                            'send_time': send_time})# + timedelta(hours=9)})

    return deque(sorted(res, key=lambda x: x['send_time']))


def get_reservation_list(user_key='', phone_number=''):
    if user_key or phone_number:
        params = {'key': API_KEY, 'kakaoUserKey': user_key, 'phoneNumber': phone_number}
        res = requests.get(base_url + '/reserv/search', params)
        if res.status_code != 200:
            return False
        res = res.json()

        if res['result'] == 'success':
            reserv_list = res['reservList']
            #for i in res['reservList']:
            #    reserv_list.append({**i['store'], **i['reserv']})

            for reserv in reserv_list:
                reserv['reservTime'] = datetime.strptime(reserv['reservTime'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
                reserv['reservTime'] += timedelta(hours=9)
                #reserv['reservTime'] += timedelta(hours=9)
            print('예약 리스트 : ', reserv_list)

            return reserv_list
        elif res['result'] == 'failed':
            print(res)
            # error_code = res['msg'].split(' : ')[1]
            return []
        else:
            return False
    else:
        return False


def check_regist(user_key='', phone_number=''):
    params = {'key': API_KEY, 'kakaoUserKey': user_key, 'phoneNumber': phone_number}
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


def reservation_cancel(reservation_id):
    res = reserv_status_edit(reservation_id, 'usercancel')
    print(res.text)
    print(res.json())
    return res.json()


def reservation_confirm(reservation_id):
    res = reserv_status_edit(reservation_id, 'reserved')
    return res.json()


def reserv_status_edit(reservation_id, status):
    params = {'key': API_KEY, 'reservId': reservation_id, 'status': status}
    res = requests.get(base_url + '/reserv/edit', params)
    return res


def reserv_match(user_key, token, person_number, phone_number):
    params = {'key': API_KEY, 'kakaoUserKey': user_key, 'reservToken': token, 'reservNumber': int(person_number), 'phoneNumber': phone_number}
    print('match send data : ')
    print(params)
    res = requests.get(base_url + '/reserv/match', params)
    print(res.json())
    return res.json()


def set_name(reserv_id, person_name):
    params = {'key': API_KEY, 'reservId': reserv_id, 'name': person_name}
    res = requests.get(base_url + '/reserv/setname', params)
    print(res.text)
    return res.json()


def get_current_status(reserv_id='', token=''):
    params = {'key': API_KEY, 'reservId': reserv_id, 'reservToken': token}
    #res = requests.get(base_url + '/reserv/getstatus', params)
    res = requests.get(base_url + '/reserv/getstatus', params)

    print(res.text)
    return res.json()


def push(reserv_id, status, title, content):
    params = {'key': API_KEY, 'reservId':reserv_id, 'status':status, 'msg':{'title': title, 'content':content}}
    res = requests.post(base_url + '/push', json=params)
    return res


def regist_user(kakao_user_key, phone_number):
    params = {'key': API_KEY, 'kakaoUserKey': kakao_user_key, 'phoneNumber': phone_number}
    res = requests.get(base_url + '/info/reg', params)
    print(res.text)
    print(res.json())
    return res.json()

def get_reservation(reservation_id):
    pass

