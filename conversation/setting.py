from conversation import *
from response import Keyboard, Response
import copy


commands = {
    '예약 확인 할래요!': reservationConfirm.initial,
    '예약 취소 할래요!': reservationCancel.initial
}
default_keyboard = ['예약 확인 할래요!', '예약 취소 할래요!']
alrim_keyword = ['확정', '취소']




def fallback_function(user_key, response):
    for command in default_keyboard:
        if response == command:
            return commands[command](user_key)
    else:
        return init_response


fallback = Response('현재는 지원하지 않는 기능입니다.', keyboard_buttons=default_keyboard)
fallback.set_function(fallback_function)

init_keyboard = Keyboard(default_keyboard)
init_keyboard.set_function(fallback_function)

init_response = Response('아차 입니다\n 무엇을 도와 드릴까요?', keyboard_buttons=default_keyboard)
init_response.set_function(fallback_function)


def get_init_response():
    return copy.deepcopy(init_response)

