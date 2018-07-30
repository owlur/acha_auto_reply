from response import Response
import DB


def initial(user_key):
    reserv_list = DB.get_reservation_list(user_key)
    button_list = list(reserv_list.values())
    print(button_list)
    resp = Response('아래의 예약 중 취소하고 싶은 예약을 선택하여 주십시오', keyboard_buttons=button_list)
    for reserv_id in reserv_list:
        resp.set_function(reserv_list[reserv_id], cancel(user_key, reserv_id))
    return resp

def cancel(user_key, reservation_id):
    message = DB.get_reservation(reservation_id) + '예약을 취소 하시겠습니까?'

    def wrapper_func(user_key):
        resp = Response(message, keyboard_buttons=['예', '아니오'])
        return resp
    return wrapper_func
