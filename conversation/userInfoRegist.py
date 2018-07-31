import DB
from response import Response
from conversation import setting


def initial(user_key):
    reserv_list = DB.get_reservation_list(user_key)
    button_list = []

    print(button_list)
    resp = Response('예약 정보 조회를 위해 휴대폰 번호를 입력하여 주세요.\n 이는 최초 1회만 실시됩니다!\n하이폰(-)은 제외하고 입력\nex)01012345678')
    for reserv in reserv_list:
        resp.set_function(reserv['button_name'], find_reservation(user_key, reserv))
    return resp


def check_regist(user_key):
    res = DB.check_regist(user_key)
    if res == 'true':
        return True
    elif res == 'false':
        return False