from conversation import setting


def initial(user_key):
    resp = setting.get_init_response()
    resp.message = '안녕하세요! 아차! 서비스는 고객들이 손쉽게 예약을 관리할 수 있도록 하고 매장 점주들에게는 효율적인 예약관리를 통해 매출 증대를 함께 고민하는 서비스 입니다.'
    return resp