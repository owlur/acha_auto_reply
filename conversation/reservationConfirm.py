"""
예약 확인
1. 예약 리스트 조회
2. 확인 완료 or 예약 취소
3. 예약 취소 시 예약 취소 진행
"""


from response import Response
from conversation.reservationCancel import cancel_confirm
from conversation import setting, userInfoRegist
import DB


def initial(user_key):
    if DB.check_regist(user_key) == 'false':
        return userInfoRegist.initial(user_key)
    reserv_list = DB.get_reservation_list(user_key)
    button_list = []
    if reserv_list:
        for reserv in reserv_list:
            date = reserv['reservTime']

            button_name = '%d월 %d일 %s'%(date.tm_mon, date.tm_mday,reserv['storeName'])
            button_list.append(button_name)
            reserv['button_name'] = button_name

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
                message = '%s 예약 정보입니다.\n성함 : %s\n시간 : %d월 %d일 %s %d시% d분\n인원 : %s' %\
                          (reservation['storeName'],reservation['reservName'],  date.tm_mon, date.tm_mday,'오후' if date.tm_hour >= 12 else '오전',
                           date.tm_hour - 12 if date.tm_hour > 12 else date.tm_hour , date.tm_min, reservation['reservNumber'])
                resp = Response(message, keyboard_buttons=['확인 완료', '예약 취소'])
                resp.message_button =['지도 보기', f"http://api.acha.io:3000/user/map?addr={reservation['storeAdress']}"]
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