from conversation import setting


def initial(user_key):
    resp = setting.get_init_response()
    resp.message = '현재 아차!는 테스트중인 서비스로 별도의 제휴신청은 받고 있지 않습니다! 작은 관심 감사합니다!'