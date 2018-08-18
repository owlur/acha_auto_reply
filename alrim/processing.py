import re
from alrim import send
from conversation import setting
import DB

template ={'FIRRM0005': "\[.+\]\n\n안녕하세요! .+ 님에게 아래와 같이 예약이 접수되었습니다.\n예약내용이 맞는지 확인 부탁드립니다!\n이름 : .+\n인원 : .+\n날짜 : .+\n\n예약 내용이 맞으실 경우 .+ 이내에 '확정' 버튼을, 아닐 경우 '취소' 버튼을 눌러주세요!\n'확정' 버튼을 누르실 경우 간편한 예약 관리 서비스 '아차'에 .+에 동의 하게 됩니다!\n이후 '아차' 플러스 친구를 통해 간편하게 예약 확인 및 취소가 가능합니다\n\n예약 번호 : [0-9]{16}"}


def reserv_regist(phone_number, store_name, person_name, person_num, date, token):
    template_code = 'FIRRM0005'
    template_parameter = {'상호명': store_name, '이름': person_name, '인원': person_num, '날짜': date, '예약번호': token, '제한시간': '30분', \
                          '법률': '개인정보의 제3자 수집 이용 제공', 'mobile_url': 'https://www.privacy.go.kr/a3sc/per/chk/examInfoViewFQ41.do', \
                          'pc_url': 'https://www.privacy.go.kr/a3sc/per/chk/examInfoViewFQ41.do'}
    return send.send_alrim(template_code, phone_number, template_parameter)


def parse_initial_reservation_alrim(user_key, command, content):

    regex = template['FIRRM0005']

    res = re.match(regex, content)
    if not res:
        print(content,'\n 템플릿 일치하지 않음')
        return False
    splited_content = content.split('\n')

    store_name = splited_content[0][1:-1]
    person_name = splited_content[4].split('이름 : ')[1]
    person_number = splited_content[5].split('인원 : ')[1]
    reserv_time = splited_content[6].split('날짜 : ')[1]
    token = splited_content[-1].split('예약 번호 : ')[1]
    print(store_name, person_name, person_number, token)
    res = DB.reserv_match(user_key, token, person_name, person_number)
    print(res)

    reserv_info = splited_content[0] + '\n' + '\n'.join(splited_content[4:7])
    if command == '확정':
        return reserv_confirm(user_key, res['statusCode'], reserv_info, res['reservId'])
    elif command == '취소':
        return reserv_cancel(user_key, res['statusCode'], reserv_info, res['reservId'])


def reserv_confirm(user_key, status_code, reserv_info, reserv_id):
    if status_code == 'reservwait':
        DB.reservation_confirm(user_key, reserv_id)
        resp = setting.get_init_response()
        resp.message = '아래의 예약이 확정 되었습니다!\n' + reserv_info
        return resp
    else:
        resp = setting.get_init_response()
        resp.message = '확정할 수 없는 예약입니다.\n(이미 확정된 예약, 취소된 예약 등)'
        return resp


def reserv_cancel(user_key, status_code, store_name, person_name, person_num, reserv_time, reserv_id):
    if status_code == 'reservwait' or status_code == 'reserved':
        pass