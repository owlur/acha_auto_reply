from response import Response, Keyboard

def find_reservation(user_key):
    return []


def reservation_confirm(user_key):

    reservation_list = find_reservation(user_key)

    if reservation_list:
        response = {'message': '아래의 예약중 확인하고 싶은 예약을 선택하여 주십시오', 'buttons': reservation_list}
    else:
        response = {'message': '현재 예약되어 있는 내용이 없습니다.'}
    return response


init = Keyboard(keyboard_buttons=['예약 확인'])
init.set_function(0, reservation_confirm)

fallback = {'message': '현재 대화 기능은 지원되지 않습니다. 다시 진행해주시기 바랍니다.'}