import re
from alrim import send


def parse_initial_reservation_alrim(content):
    """
    content
    [#{상호명}] 안녕하세요 #{이름} 고객님! #{상호명}입니다.
고객님에게 아래와 같이 예약이 접수 되었습니다.
이름 : #{이름}
인원 : #{인원}
시간 : #{날짜}
위의 예약사항이 맞을 경우 '확정' 버튼을 아닐 경우 '취소'버튼을 클릭해 주십시오
이후 '아차' 플러스친구를 이용해 간편하게 예약 확인 및 취소가 가능합니다.
    """
    print(content)
    regex = "\[.+\] 안녕하세요 .+ 고객님!\n아래 접수하신 내용이 맞으신가요?\n이름 : .+\n인원 : .+\n시간 : .+\n\n위와같이 예약내용이 맞다면 .+ 내에 '확정' 버튼을, 아닐경우 '취소' 버튼을 눌러주세요! \[[0-9]{16}\]"

    res = re.match(regex, content)
    if not res:
        return False
    print(res.group())
    splited_content = content[1:].split('\n')


def reserv_regist(phone_number, store_name, person_name, person_num, date, token):
    template_code = 'FIRRM0003'
    template_parameter = {'상호명': store_name, '이름': person_name, '인원': person_num, '날짜': date, '예약번호': token, '제한시간': '30분'}
    return send.send_alrim(template_code, phone_number, template_parameter)


parse_initial_reservation_alrim('')