import re


def parse_initial_reservation_alrim(content):
    """content
    [#{상호명}] 안녕하세요 #{이름} 고객님! #{상호명}입니다.
고객님에게 아래와 같이 예약이 접수 되었습니다.
이름 : #{이름}
인원 : #{인원}
시간 : #{날짜}
위의 예약사항이 맞을 경우 '확정' 버튼을 아닐 경우 '취소'버튼을 클릭해 주십시오
이후 '아차' 플러스친구를 이용해 간편하게 예약 확인 및 취소가 가능합니다.
    """
    regex = "[.+] 안녕하세요 .+ 고객님! .+입니다.\n고객님에게 아래와 같이 예약이 접수 되었습니다.\n이름 : .+\n인원 : .+\n시간 : .+\n위의 예약사항이 맞을 경우 '확정' 버튼을 아닐 경우 '취소'버튼을 클릭해 주십시오\n이후 '아차' 플러스친구를 이용해 간편하게 예약 확인 및 취소가 가능합니다."
    res = re.match(regex, content)
    if not res:
        return False
    print(res.group())
    splited_content = content.split[1:]('\n')



parse_initial_reservation_alrim('')