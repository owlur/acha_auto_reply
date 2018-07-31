from response import Response
from conversation import setting
import DB


def initial(user_key):
    reserv_list = DB.get_reservation_list(user_key)
    button_list = []
    for reserv in reserv_list:
        date = reserv['reservTime']
        button_name = '%d월 %d일 %s'%(date.tm_mon, date.tm_mday,reserv['storeName'])
        button_list.append(button_name)
        reserv['button_name'] = button_name
    print(button_list)
    resp = Response('아래의 예약 중 취소하고 싶은 예약을 선택하여 주십시오', keyboard_buttons=button_list)
    for reserv in reserv_list:
        resp.set_function(reserv['button_name'], cancel(user_key, reserv))
    return resp


def cancel(user_key, reservation):
    def wrapper_func(user_key):
        print(reservation)
        message = reservation['button_name'] + '예약을 취소 하시겠습니까?'
        resp = Response(message, keyboard_buttons=['예', '아니오'])
        resp.set_function('예', cancel_confirm(user_key, reservation))
        return resp
    return wrapper_func


def cancel_confirm(user_key, reservation):
    #예약 취소 API 호출해야함
    def wrapper_func(user_key):
        message = reservation['button_name'] + '예약이 취소 되었습니다.'
        resp = setting.get_init_response()
        resp.message = message
        return resp
    return wrapper_func