"""
예약 확인
1. 예약 리스트 조회
2. 확인 완료 or 예약 취소
3. 예약 취소 시 예약 취소 진행
"""


from response import Response
from conversation.reservationCancel import cancel_confirm
from conversation import setting, userInfoRegist
import DB, utils


def initial(user_key):
    if DB.check_regist(user_key) == 'false':
        return userInfoRegist.initial(user_key)

    reserv_list = DB.get_reservation_list(user_key)

    if reserv_list:
        reserv_list.sort(key=lambda x:x['reservTime'])

        button_list = utils.generate_button(reserv_list)

        print(button_list)
        resp = Response('아래의 예약 중 확인하고 싶은 예약을 선택하여 주십시오', keyboard_buttons=button_list)
        resp.set_function(find_reservation(user_key, reserv_list))
        return resp
    else:
        resp = setting.get_init_response()
        resp.message = '현재 예약되어 있는 내용이 없습니다.'
        return resp


def find_reservation(outer_user_key, reservation_list):
    def wrapper_func(inner_user_key, response):
        for reservation in reservation_list:
            if reservation['button_name'] == response:
                date = reservation['reservTime']
                message = '선택하신 예약 정보입니다!!    \n\n[예약 정보]\n- 성함 : %s\n- 인원 : %s\n- 날짜 : %s\n\n[매장 정보]\n- 매장 이름 : %s\n- 매장 연락처 : %s'\
                          %(reservation['reservName'], reservation['reservNumber'], utils.datetime2str(date), \
                            reservation['storeName'], reservation['storePhoneNumber'])

                resp = Response(message, keyboard_buttons=['확인 완료', '예약 취소'])
                resp.message_button =['지도 보기', "http://api.acha.io:3000/user/map?addr=%s&storeName=%s&detailAddress=%s" %
                                      (reservation['roadAddress'], reservation['storeName'], reservation['detailAddress'])]
                resp.set_function(reservation_cancel(inner_user_key,reservation))
                return resp
        else:
            return setting.init_response
    return wrapper_func


def reservation_cancel(outer_user_key, reservatoin):
    def wrapper_func(inner_user_key, response):
        if response == '예약 취소':
            message = reservatoin['button_name'] + ' 예약을 정말로 취소하시겠습니까?'
            resp = Response(message, keyboard_buttons=['예', '아니오'])
            resp.set_function(cancel_confirm(inner_user_key, reservatoin))
            return resp
        else:
            return setting.init_response
    return wrapper_func


def get_phone_number():
    pass