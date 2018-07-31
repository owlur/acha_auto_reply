from conversation import *
from response import Keyboard, Response
import copy


commands = {
    '예약 확인': reservationConfirm.initial,
    '예약 취소': reservationCancel.initial
}
default_keyboard = ['예약 확인', '예약 취소']

"""
fallback = Response('현재는 지원하지 않는 기능입니다.', keyboard_buttons=default_keyboard)
for command in default_keyboard:
    fallback.set_function(command, commands[command])
"""


def fallback_function(user_key, response):
    for command in commands:
        if response == command:
            return commands[command]()


fallback = Response('현재는 지원하지 않는 기능입니다.', keyboard_buttons=default_keyboard)
fallback.set_function(fallback_function)

init_keyboard = Keyboard(default_keyboard)
init_keyboard.set_function(fallback_function)
"""for command in commands:
    init_keyboard.set_function(command, commands[command])"""

init_response = Response('아차 입니다\n 무엇을 도와 드릴까요?', keyboard_buttons=default_keyboard)
"""for command in commands:
    init_response.set_function(command, commands[command])"""
init_response.set_function(fallback_function)


def get_init_response():
    return copy.deepcopy(init_response)

