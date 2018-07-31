from response import Response
from conversation.reservationCancel import cancel
from conversation import setting
import DB


def initial(user_key):
    reserv_list = DB.get_reservation_list(user_key)
    button_list = []
    for reserv in reserv_list:
        date = reserv['reserTime']
        button_name = '%d월 %d일 %s'%(date.tm_mon, date.tm_mday,reserv['storeName'])
        button_list.append(button_name)
        reserv['button_name'] = button_name

    button_list = list(reserv_list.values())
    print(button_list)
    resp = Response('아래의 예약 중 확인하고 싶은 예약을 선택하여 주십시오', keyboard_buttons=button_list)
    for reserv in reserv_list:
        resp.set_function(reserv['button_name'], find_reservation(user_key, reserv))
    return resp


def find_reservation(user_key, reservation):
    def wrapper_func(user_key):
        message = '%s 예약 정보입니다.\n성함 : %s\n시간 : %d월 %d일 %d:%d\n인원 : %d'%\
                  (reservation['storeName'],reservation['reservName'], reservation['reservTime'].tm_mon, reservation['reservTime'].tm_mday,
                   reservation['reservTime'].tm_hour, reservation['reservTime'].tm_min, reservation['reservNumber'])
        resp = Response(message, keyboard_buttons=['확인 완료', '예약 취소'])
        #resp.set_function('확인 완료', setting.init_response)
        resp.set_function('예약 취소', cancel(user_key,reservation['reservId']))
        return resp
    return wrapper_func


def get_phone_number():
    pass