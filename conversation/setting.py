from conversation import *
from response import Keyboard, Response
from conversation import setting


commands = {
    '예약 확인': reservationConfirm.initial,
    '예약 취소': reservationCancel.initial
}
default_keyboard = ['예약 확인', '예약 취소']


fallback = Response('현재는 지원하지 않는 기능입니다.', keyboard_buttons=default_keyboard)
for command in default_keyboard:
    fallback.set_function(command, commands[command])


init_keyboard = Keyboard(setting.default_keyboard)
for command in setting.commands:
    keyboard.set_function(command, setting.commands[command])

init_response = Response('아차 입니다\n 무엇을 도와 드릴까요?', keyboard_buttons=setting.default_keyboard)
for command in setting.commands:
    init_response.set_function(command, setting.commands[command])