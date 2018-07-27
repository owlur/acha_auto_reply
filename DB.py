import requests
from json import dump

base_url = 'http://api.acha.io/user'


def get_reservation_list(user_key):
    #params = {'user_key': user_key}
    #res = requests.get(base_url + '/reservation/search', params)
    #res = dump(res)
    return [{'name': '9월 30일 맥도날드', 'idx': '245324'}]