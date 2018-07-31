import requests
from json import dump

base_url = 'http://api.acha.io:3000/user'
API_KEY = '33233C0EB2C9CA56566FD7D503F100ABDBE012306B4EB812C3C9E83129E8495D'


def get_reservation_list(user_key):
    #params = {key: API_KEY, 'kakaoUserKey': user_key}
    #res = requests.get(base_url + '/reservation/search', params)
    #res = dump(res)

    """
    if res['result'] == 'success':
        reserv_list = res['reservList']
    """
    return {'245324': '9월 30일 맥도날드', '242324': '9월 20일 한옥집'}


def get_reservation(reservation_id):
    reserv_list = {'245324': '9월 30일 맥도날드', '242324': '9월 20일 한옥집'}

    return reserv_list[reservation_id]