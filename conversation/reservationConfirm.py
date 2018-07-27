from response import Response
import DB


def initial(user_key):
    button_list = ['8월12일 맥도날드 선릉점', '8월 13일 한옥집']
    resp = Response('아래의 예약 중 확인하고 싶은 예약을 선택하여 주십시오', keyboard_buttons=button_list)
    for button in button_list:
        resp.set_function(button, find_reservation(user_key, button))
    return resp


def find_reservation(user_key, reservation_idx):
    message = reservation_idx

    def wrapper_func(user_key):
        resp = Response(message)
        return resp
    return wrapper_func


def get_phone_number():
    pass








fallback = {'message': '현재 대화 기능은 지원되지 않습니다. 다시 진행해주시기 바랍니다.'}

command_list = ['예약 확인', '예약 취소']
