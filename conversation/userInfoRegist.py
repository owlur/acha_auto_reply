import re

import DB
from response import Response

from conversation import setting


def initial(user_key):
    resp = Response('안녕하세요! 아차 서비스를 처음 이용하시네요. 고객님의 간편한 서비스 이용을 위해 아래의 내용에 대한 동의가 필요합니다.'
                    '아차 개인정보 수집이용'
                    '- 이용 목적 : 회원 식별/예약 확인,취소 및 결제 등'
                    '- 수집 항목 : 고객명, 휴대폰번호, 예약정보, 결제정보'
                    '- 보유 기간 : 최종서비스이용시점으로부터 5년'
                    '- 수탁 업체 : 젊은친구들'
                    '- 위탁 업무 : 카카오톡 기반 예약 서비스 제공'
                    '- 톡주문 서비스 동의 철회: help@acha.io>아차 서비스 동의 철회 요청'
                    '동의하시겠습니까?')
    resp.buttons = ['동의', '미동의(서비스 이용 불가)']
    #resp = Response('예약 정보 조회를 위해 휴대폰 번호를 입력하여 주세요.\n 이는 최초 1회만 실시됩니다!\n하이폰(-)은 제외하고 입력\nex)01012345678')
    resp.set_function(receive_phone_number(user_key))
    return resp


def request_phone_number(outer_user_key):
    def wrapper_function(inner_user_key, response):
        if response == '동의':
            resp = Response('예약 정보 조회를 위해 휴대폰 번호를 입력하여 주세요.\n 이는 최초 1회만 실시됩니다!\n하이폰(-)은 제외하고 입력\nex)01012345678')
            resp.set_function(receive_phone_number(inner_user_key))

        else:
            resp = setting.get_init_response()
        return resp
    return wrapper_function


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