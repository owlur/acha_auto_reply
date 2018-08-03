import re

import DB
from response import Response

from conversation import setting


def initial(user_key):
    resp = Response('예약 정보 조회를 위해 휴대폰 번호를 입력하여 주세요.\n 이는 최초 1회만 실시됩니다!\n하이폰(-)은 제외하고 입력\nex)01012345678')
    resp.set_function()
    return resp


def receive_phone_number(inner_user_key):
    def wrapper_function(outer_user_key, response):
        p = re.compile('01{1}[016789]{1}[0-9]{7,8}')

        regres = p.match(response)
        if regres and regres.end() == len(response):
            DB.user_regist(outer_user_key, response)
            resp = setting.get_init_response()
            resp.message = '정보가 등록되었습니다. 아차를 이용하는 매장에서 등록된 예약 정보를 확인 가능합니다.'
        else:
            resp = setting.get_init_response()
            resp.message = '휴대폰 번호만 정확히 입력해 주십시오.\nex)01012345678'

        return resp
    return wrapper_function


def check_regist(user_key):
    res = DB.check_regist(user_key)
    if res == 'true':
        return True
    elif res == 'false':
        return False