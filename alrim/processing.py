import re
from alrim import send
from conversation import setting
import DB


def reserv_regist(phone_number, store_name, person_name, person_num, date, token):
    """
    최초 예약 등록 알림톡 전송
    :param phone_number:
    :param store_name:
    :param person_name:
    :param person_num:
    :param date:
    :param token:
    :return:
    """
    template_code = 'FIRRM0006'
    template_parameter = {'상호명': store_name, '이름': person_name, '인원': person_num, '날짜': date, '예약번호': token, '제한시간': '30분', \
                          '법률': '개인정보의 제3자 수집 이용 제공', 'mobile_url': 'acha.io:5000/PrivacyPolicy', \
                          'pc_url': 'acha.io:5000/PrivacyPolicy'}
    return send.send_alrim(template_code, phone_number, template_parameter)


def alrim_response_parsing(session, command, content):
    """
    메시지를 수신하였을 때 일치하는 알림톡 템플릿이 존재하는지 확인 후 템플릿에 해당하는 처리 함수 호출
    :param session:
    :param command:
    :param content:
    :return:
    """
    for template_code in templates:
        regex = templates[template_code][0]
        if re.match(regex, content):
            splited_content = list(filter(lambda x: x, content.split('\n')))
            session.next = setting.init_response
            return templates[template_code][1](session, command, splited_content)
    print(content,'\n 템플릿 일치하지 않음')
    return False


def initial_alrim_response(session, command, splited_content):
    """
    최초 전송하는 알림톡 응답시
    :param session:
    :param command:
    :param splited_content:
    :return:
    """
    store_name = splited_content[0][1:-1]
    person_name = splited_content[3].split('이름 : ')[1]
    person_number = splited_content[4].split('인원 : ')[1]
    reserv_time = splited_content[5].split('날짜 : ')[1]
    token = splited_content[-1].split('예약 번호 : ')[1]

    res = DB.reserv_match(session.user_key, token, person_name, person_number)

    reserv_info = splited_content[0] + '\n' + '\n'.join(splited_content[3:6])
    if command == '확정':
        return reserv_confirm(session, res['statusCode'], reserv_info, res['reservId'])
    elif command == '취소':
        return reserv_cancel(session, res['statusCode'], reserv_info, res['reservId'])


def interval_alrim_response(session, command, splited_content):
    """
    주기에 따라 보내는 알림톡 응답시
    :param session:
    :param command:
    :param splited_content:
    :return:
    """
    store_name = splited_content[0][1:-1]
    person_name = splited_content[2].split('이름 : ')[1]
    reserv_time = splited_content[3].split('날짜 : ')[1]
    person_number = splited_content[4].split('인원 : ')[1]
    token = splited_content[-1].split('예약 번호 : ')[1]

    res = DB.reserv_match(session.user_key, token, person_name, person_number)

    reserv_info = splited_content[0] + '\n' + '\n'.join(splited_content[2:5])
    if command == '예약 취소':
        return reserv_cancel(session, res['statusCode'], reserv_info, res['reservId'])


def reserv_confirm(session, status_code, reserv_info, reserv_id):
    resp = setting.get_init_response()
    if status_code == 'reservwait':
        DB.reservation_confirm(session.user_key, reserv_id)
        resp.message = '아래의 예약이 확정 되었습니다!\n' + reserv_info
    else:
        resp.message = '확정할 수 없는 예약입니다.\n(이미 확정된 예약, 취소된 예약 등)'
    return resp.get_response()


def reserv_cancel(session, status_code, reserv_info, reserv_id):
    if status_code == 'reservwait' or status_code == 'reserved':
        resp = setting.get_init_response()
        resp.message = '정말로 아래의 예약을 취소 하시겠습니까?\n' + reserv_info
        resp.next_function = reserv_cancel_confirm(reserv_id)
        resp.buttons = ['네!', '아니요 괜찮아요!']
        session.next = resp
        return resp.get_response()


def reserv_cancel_confirm(reserv_id):
    def wrapper_function(user_key, content):
        if content == '네!':
            DB.reservation_cancel(user_key, reserv_id)
            resp = setting.get_init_response()
            resp.message = '예약이 정상적으로 취소되었습니다!'
            return resp
        else:
            return setting.init_response
    return wrapper_function


templates ={'FIRRM0006': ( ("\[.+\]\n\n"
                            "안녕하세요! .+ 님에게 아래와 같이 예약이 접수되었습니다.\n"
                            "예약내용이 맞는지 확인 부탁드립니다!\n"
                            "이름 : .+\n"
                            "인원 : .+\n"
                            "날짜 : .+\n\n"
                            "예약 내용이 맞으실 경우 .+ 이내에 '확정' 버튼을, 아닐 경우 '취소' 버튼을 눌러주세요!\n\n"
                            "'확정' 버튼을 누르실 경우 간편한 예약 관리 서비스 '아차'에 .+에 동의 하게 됩니다!\n\n"
                            "이후 '아차' 플러스 친구를 통해 간편하게 예약 확인 및 취소가 가능합니다\n\n"
                            "예약 번호 : [0-9]{16}"),
                           initial_alrim_response),
           'RRM0003': ( ("\[.+\]\n\n"
                         "안녕하세요! 곧 .+님이 .+에 예약하신 시간입니다!\n"
                         "이름 : .+\n"
                         "날짜 : .+\n"
                         "인원 : .+\n\n"
                         "만약 해당 예약의 취소를 원하실 경우 아래의 '예약 취소' 버튼을 통해 간편하게 예약을 취소하실 수 있습니다.\n\n"
                         "잠시 후 .+에서 뵙겠습니다!\n\n"
                         "예약 번호 : [0-9]{16}"),
                        interval_alrim_response),
           'RRM0004': ( ("\[.+\]\n\n"
                         "안녕하세요! .+님이 예약하신 날짜까지 .+ 남았습니다!\n"
                         "이름 : .+\n"
                         "날짜 : .+\n"
                         "인원 : .+\n\n"
                         "만약 해당 예약의 취소를 원하실 경우 아래의 '예약 취소' 버튼을 통해 간편하게 예약을 취소하실 수 있습니다!\n\n"
                         "예약 번호 : [0-9]{16}"),
                        interval_alrim_response)
            }
