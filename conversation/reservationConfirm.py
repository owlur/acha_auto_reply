from response import Response
from conversation.reservationCancel import cancel_confirm
from conversation import setting
import DB


"""def initial(user_key):
    reserv_list = DB.get_reservation_list(user_key)
    button_list = []
    for reserv in reserv_list:
        date = reserv['reservTime']
        button_name = '%d월 %d일 %s'%(date.tm_mon, date.tm_mday,reserv['storeName'])
        button_list.append(button_name)
        reserv['button_name'] = button_name

    print(button_list)
    resp = Response('아래의 예약 중 확인하고 싶은 예약을 선택하여 주십시오', keyboard_buttons=button_list)
    for reserv in reserv_list:
        resp.set_function(reserv['button_name'], find_reservation(user_key, reserv))
    return resp
"""

def initial(user_key):
    reserv_list = DB.get_reservation_list(user_key)
    button_list = []
    for reserv in reserv_list:
        date = reserv['reservTime']
        button_name = '%d월 %d일 %s'%(date.tm_mon, date.tm_mday,reserv['storeName'])
        button_list.append(button_name)
        reserv['button_name'] = button_name

    print(button_list)
    resp = Response('아래의 예약 중 확인하고 싶은 예약을 선택하여 주십시오', keyboard_buttons=button_list)
    resp.set_function(find_reservation2(user_key, reserv))
    return resp


"""def find_reservation(user_key, reservation):
    def wrapper_func(user_key):
        message = '%s 예약 정보입니다.\n성함 : %s\n시간 : %d월 %d일 %d:%d\n인원 : %s'%\
                  (reservation['storeName'],reservation['reservName'], reservation['reservTime'].tm_mon, reservation['reservTime'].tm_mday,
                   reservation['reservTime'].tm_hour, reservation['reservTime'].tm_min, reservation['reservNumber'])
        resp = Response(message, keyboard_buttons=['확인 완료', '예약 취소'])
        #resp.set_function('확인 완료', setting.init_response)
        resp.set_function('예약 취소', cancel(user_key,reservation))
        return resp
    return wrapper_func
"""

def find_reservation2(outer_user_key, reservation_list):
    def wrapper_func(inner_user_key, response):
        for reservation in reservation_list:
            if reservation['button_name'] == response:
                message = '%s 예약 정보입니다.\n성함 : %s\n시간 : %d월 %d일 %d:%d\n인원 : %s'%\
                          (reservation['storeName'],reservation['reservName'], reservation['reservTime'].tm_mon, reservation['reservTime'].tm_mday,
                           reservation['reservTime'].tm_hour, reservation['reservTime'].tm_min, reservation['reservNumber'])
                resp = Response(message, keyboard_buttons=['확인 완료', '예약 취소'])
                #resp.set_function('확인 완료', setting.init_response)
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


def get_phone_number():
    pass