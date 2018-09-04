from conversation import setting


def initial(user_key):
    resp = setting.get_init_response()
    resp.message = '현재 아차!는 테스트중으로 무료로 서비스를 제공하고 있습니다. 관련 문의는 상담용 플러스친구(http://pf.kakao.com/_xfxbxnxhj)를 통해 문의하실 수 있습니다.'
    return resp