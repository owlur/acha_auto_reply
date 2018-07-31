from response import Response
from conversation.reservationCancel import cancel
from conversation import setting
import DB


def initial(user_key):

    reserv_list = DB.get_reservation_list(user_key)
    button_list = list(reserv_list.values())
    print(button_list)
    resp = Response('아래의 예약 중 확인하고 싶은 예약을 선택하여 주십시오', keyboard_buttons=button_list)
    for reserv_id in reserv_list:
        resp.set_function(reserv_list[reserv_id], find_reservation(user_key, reserv_id))
    return resp


def find_reservation(user_key, reservation_idx):
    def wrapper_func(user_key):
        message = DB.get_reservation(reservation_idx)
        resp = Response(message, keyboard_buttons=['확인 완료', '예약 취소'])
        #resp.set_function('확인 완료', setting.init_response)
        resp.set_function('예약 취소', cancel(user_key,reservation_idx))
        return resp
    return wrapper_func


def get_phone_number():
    pass