import DB
from response import Response
from conversation import setting



question_list = ['delicious', 'service', 'revisit_coupon', 'comment']


def feedback_response(session, command, splited_content, phone_number_dict):
    token = splited_content[-1].split(' : ')[1]
    if command == '네':

        question = feedback_list[question_list[0]]
        if type(question) == str:
            resp = Response(question)
        else:
            resp = Response(question[0], keyboard_buttons=list(question[1]))

        resp.set_function(feedback_step(1))
        session.next = resp

        return (resp.get_response(), '피드백 참여', token)
    else:
        resp = setting.get_init_response()
        return (resp.get_response(), '피드백 불참', token)


def feedback_step(step):
    def wrapper_func(user_key, content):
        if step == len(question_list):
            resp = setting.get_init_response()
            resp.message = '피드백이 완료 되었습니다!'
        else:
            #content 저장
            question = feedback_list[question_list[step]]
            if type(question) == str:
                resp = Response(question)
            else:
                resp = Response(question[0], keyboard_buttons=list(question[1]))

            resp.set_function(feedback_step(step + 1))

        return resp
    return wrapper_func


feedback_list = {
    'delicious' : ('드셨던 식사의 맛이 어떠셨나요? ( 1~5 점 중 선택)', ('1','2','3','4','5')),
    'service': ('매장의 서비스 및 친절도는 어떠셨나요? ( 1~5 점 중 선택)', ('1','2','3','4','5')),
    'revisit': ('추후 매장에 재방문 하실 의향이 있으십니까?', ('네', '아니오')),
    'revisit_coupon': ('추후 매장에 재방문 하실 의향이 있으십니까? (이 질문의 응답에 따라 본 매장의 쿠폰 혹은 다른 매장의 쿠폰이 지급됩니다.)', ('네', '아니오')),
    'strength': '손님이 생각하는 매장의 좋았던 점을 작성하여 주세요',
    'weakness': '손님이 생각하는 매장의 불편했던 점을 작성하여 주세요',
    'comment': '매장에 전달하고 싶은 말을 작성해주세요'
}