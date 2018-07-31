import requests
from json import dump
import time


base_url = 'http://api.acha.io:3000/user'
API_KEY = '33233C0EB2C9CA56566FD7D503F100ABDBE012306B4EB812C3C9E83129E8495D'


def get_reservation_list(user_key='', phone_number=''):
    if user_key or phone_number:
        params = {'key': API_KEY, 'kakaoUserKey': user_key, 'phoneNumber': phone_number}
        res = requests.get(base_url + '/reserv/search', params)
        if res.status_code != 200:
            return False
        res = res.json()

        if res['result'] == 'success':
            reserv_list = res['reservList']
            for reserv in reserv_list:
                reserv['reservTime'] = time.strptime(reserv['reservTime'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
            print(res['reservList'])
            return res['reservList']
        else:
            print(res)
    else:
        return False


def check_regist(user_key):
    params = {'key': API_KEY, 'kakaoUserKey': user_key}
    res = requests.get(base_url + '/info/regCheck', params)
    if res.status_code != 200:
        return False

    res = res.json()
    return res['isReg']

def get_reservation(reservation_id):
    pass