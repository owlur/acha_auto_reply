"""
예약 취소
1. 예약 리스트 조회
2. 취소하고 싶은 예약 선택
3. 취소 확정 or 취소
"""

from response import Response
from conversation import setting, userInfoRegist
import DB, utils


def initial(user_key):
    if DB.check_regist(user_key) == 'false':
        return userInfoRegist.initial(user_key)

    reserv_list = DB.get_reservation_list(user_key)

    if reserv_list:
        reserv_list.sort(key=lambda x: x['reservTime'])
        button_list = utils.generate_button(reserv_list)
        """for reserv in reserv_list:
            date = reserv['reservTime']
            button_name = '%d월 %d일 %s'%(date.month, date.day,reserv['storeName'])
            button_list.append(button_name)
            reserv['button_name'] = button_name"""
        print(button_list)
        resp = Response('아래의 예약 중 취소하고 싶은 예약을 선택하여 주십시오', keyboard_buttons=button_list)
        resp.set_function(cancel(user_key, reserv_list))
        return resp
    else:
        resp = setting.get_init_response()
        resp.message = '현재 예약되어 있는 내용이 없습니다.'
        return resp


def cancel(outer_user_key, reservation_list):
    def wrapper_func(inner_user_key, response):
        for reservation in reservation_list:
            if reservation['button_name'] == response:
                date = reservation['reservTime']
                message = '정말로 아래의 예약을 취소하시겠습니까?.\n[예약 정보]\n- 성함 : %s\n- 인원 : %s\n- 날짜 : %s\n\n[매장 정보]\n- 매장 이름 : %s\n- 매장 연락처 : %s' \
                          % (reservation['reservName'], reservation['reservNumber'], utils.datetime2str(date), \
                             reservation['storeName'], reservation['storePhoneNumber'])
                #message = reservation['button_name'] + '예약을 정말로 취소 하시겠습니까?'
                resp = Response(message, keyboard_buttons=['예', '아니오'])
                resp.set_function(cancel_confirm(inner_user_key,reservation))
                return resp
        else:
            return setting.init_response

    return wrapper_func


def cancel_confirm(user_key, reservation):
    #예약 취소 API 호출해야함
    def wrapper_func(user_key, response):
        if response == '예':
            DB.reservation_cancel(reservation['reservUUID'])
            DB.push(reservation['reservUUID'], 'usercancel', '고객님이 예약을 취소하였습니다.', '자세한 내용은 앱에서 확인 부탁드립니다.')
            message = reservation['button_name'] + '예약이 취소 되었습니다.'
            resp = setting.get_init_response()
            resp.message = message
            return resp
        else:
            return setting.init_response
    return wrapper_func