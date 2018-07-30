import requests
from json import dump

base_url = 'http://api.acha.io/user'


def get_reservation_list(user_key):
    #params = {'user_key': user_key}
    #res = requests.get(base_url + '/reservation/search', params)
    #res = dump(res)
    return {'245324': '9월 30일 맥도날드', '242324': '9월 20일 한옥집'}


def get_reservation(reservation_id):
    reserv_list = {'245324': '9월 30일 맥도날드', '242324': '9월 20일 한옥집'}

    return reserv_list[reservation_id]