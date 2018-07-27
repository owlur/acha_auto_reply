from conversation import *
from response import Response

commands = {
    '예약 확인': reservationConfirm.initial
}
default_keyboard = ['예약 확인']


fallback = Response('현재는 지원하지 않는 기능입니다.')