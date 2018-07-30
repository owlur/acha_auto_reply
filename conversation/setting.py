from conversation import *
from response import Response

commands = {
    '예약 확인': reservationConfirm.initial,
    '예약 취소': reservationCancel.initial
}
default_keyboard = ['예약 확인', '예약 취소']


fallback = Response('현재는 지원하지 않는 기능입니다.', keyboard_buttons=default_keyboard)
for command in default_keyboard:
    fallback.set_function(command, commands[command])