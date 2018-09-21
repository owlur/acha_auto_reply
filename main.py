from flask import Flask, send_from_directory
from flask_restful import Resource, Api, reqparse
from conversation import setting
from session import Session
from alrim import processing, send
from datetime import datetime, timedelta
import time
import DB, utils
from multiprocessing import Process
from collections import deque
import logging
from logging.handlers import RotatingFileHandler
from threading import Timer


app = Flask(__name__, static_folder='page')
api = Api(app)

message_parser = reqparse.RequestParser()
message_parser.add_argument('user_key')
message_parser.add_argument('type')
message_parser.add_argument('content')

reserv_token = []
sessions = {}
session_queue = []
regist_queue = deque([])
check_queue = deque([])


def interval_alrim_process():
    """
    1분 간격으로 보낼 알림이 있는지 체크
    5분 간격으로 새로운 알림 리스트 요청 -> 이때 10분치의 알림 받아옴
    """
    DB.local_initilize()
    five_minute_check = 0
    last_alrim_time = datetime.now()
    while True:
        one_minute_check = time.time()
        now = datetime.now()
        if time.time() - five_minute_check >= 300:
            five_minute_check = time.time()
            alrim_queue = DB.get_alrim_list(now - timedelta(minutes=1), minute=10)
            """feedback_queue = DB.get_feedback_list(now - timedelta(minutes=1))
            total_queue = deque([])
            for i in range(len(alrim_queue + feedback_queue)):
                if alrim_queue[0]['send_time'] <= last_alrim_time:
                    alrim_queue.popleft()
                elif feedback_queue[0]['send_time'] < last_alrim_time:
                    feedback_queue.popleft()
                elif alrim_queue[0]['send_time'] <= feedback_queue[0]['send_time']:
                    total_queue.append(alrim_queue.popleft())
                else:
                    total_queue.append(feedback_queue.popleft())
            """
            while alrim_queue and alrim_queue[0]['send_time'] < last_alrim_time:
                alrim_queue.popleft()
            #while total_queue and total_queue[0]['send_time'] <= last_alrim_time:
            #    total_queue.popleft()
            if alrim_queue:
                print(datetime.now(), '보낼 알림들: ', alrim_queue)

        # 지금 보낼알림이 있는지 확인
        while alrim_queue and alrim_queue[0]['send_time'] < now:
            alrim_info = alrim_queue.popleft()
            print('보낸 알림: ', alrim_info)
            res = send.send_interval_alrim(alrim_info['phone_number'], alrim_info['store_name'],
                                           alrim_info['person_name'],
                                           alrim_info['person_num'], alrim_info['reserv_date'],
                                           alrim_info['until_time'],
                                           alrim_info['address'], alrim_info['token'])
            print('알림톡 응답: ', res)
            logger.info('SEND_INTERVAL_ALRIM:params = %s, result = %s' % (alrim_info,res))

        last_alrim_time = now

        time.sleep(60 - (time.time() - one_minute_check))


class Keyboard(Resource):
    def get(self):
        resp = setting.init_keyboard
        print(resp.buttons)
        return {'type': resp.type, 'buttons': list(resp.buttons)}


class Message(Resource):
    def post(self):
        # 세션 구분
        # 다음 함수 호출

        args = message_parser.parse_args()

        user_key = args['user_key']
        type = args['type']
        content = args['content']

        if not sessions.get(user_key):
            sessions[user_key] = Session(user_key)
        else:
            session_queue.remove(user_key)
        session_queue.append(user_key)

        content_parse = content.split('\n')
        if len(content_parse) > 2 and not content_parse[1] and content_parse[0] in setting.alrim_keyword:
            logger.info('알림톡 응답 수신:%s:%s' % (user_key, content_parse[0]))
            res = processing.alrim_response_parsing(sessions[user_key], content_parse[0],
                                                    '\n'.join(content_parse[2:]))

            if res[1] == '최초 확정':
                for reserv in regist_queue:
                    if reserv[0] == res[2]:
                        regist_queue.remove(reserv)
                        break
                else:
                    print('예약등록큐에 존재하지 않는 예약번호 입니다. %s', res[2])
            print(res)
            logger.info('RESPONSE:%s:request = %s, response = %s' % (user_key, content, res[0]))
            if res[0]:
                return res[0]

        response = sessions[user_key].receive_message(type, content)
        logger.info('RESPONSE:%s:request = %s, response = %s' % (user_key, content, response))
        return response


class Friend(Resource):
    def get(self):
        return {'message': 'test'}

    def post(self):
        args = message_parser.parse_args()
        user_key = args['user_key']
        return {'message': user_key}


class FriendDelete(Resource):
    def delete(self, user_key):
        return {'message': user_key}


class ChatRoom(Resource):
    def delete(self, user_key):
        return {'message': user_key}


reserv_parser = reqparse.RequestParser()
reserv_parser.add_argument('phoneNumber')
reserv_parser.add_argument('storeName')
reserv_parser.add_argument('reservName')
reserv_parser.add_argument('reservNumber')
reserv_parser.add_argument('reservDate')
reserv_parser.add_argument('reservToken')
reserv_parser.add_argument('reservId')
reserv_parser.add_argument('storePhoneNumber')


class ReservRegist(Resource):
    def post(self):
        args = reserv_parser.parse_args()
        dt = datetime.fromtimestamp(int(args['reservDate']) / 1000)
        args['reservDate'] = utils.datetime2str(dt)
        alrim_res = processing.reserv_regist(args['phoneNumber'], args['storeName'], args['reservName'], args['reservNumber'],
                                 args['reservDate'], args['reservToken'], args['storePhoneNumber'])
        print(alrim_res)
        if alrim_res:
            check_queue.append((args['reservId'], datetime.now() + timedelta(minutes=1), alrim_res['message']['requestId']))
            #regist_queue.append((args['reservId'], datetime.now() + timedelta(minutes=30)))
        print(args)


class PrivacyPolicy(Resource):
    def get(self):
        return send_from_directory('page', 'PrivacyPolicy.html')


api.add_resource(Keyboard, '/keyboard')
api.add_resource(Message, '/message')
api.add_resource(Friend, '/friend')
api.add_resource(FriendDelete, '/friend/<user_key>')
api.add_resource(ChatRoom, '/chat_room/<user_key>')
api.add_resource(ReservRegist, '/reserv/regist')
api.add_resource(PrivacyPolicy, '/PrivacyPolicy')


def check_regist():
    start = time.time()
    while check_queue and check_queue[0][1] < datetime.now():
        request_id = check_queue[0][2]
        alrim_res = send.get_alrim_status(request_id)
        alrim_result_code = alrim_res['resultCode']
        if alrim_result_code == '1000':
            reserv = check_queue.popleft()
            print('정상 전송', reserv[0], reserv[2])
            regist_queue.append((reserv[0], reserv[1] + timedelta(minutes=29)))
        elif alrim_result_code == '2001':
            # 카톡이 없어서 자동 확정
            reserv = check_queue.popleft()
            print('카톡 없음', reserv[0], reserv[2])
            db_res = DB.reservation_confirm(reserv[0])
            # 확정알림을 서버에 보내줘야함
        elif alrim_result_code == '1002':
            # 없는 번호일 경우 자동 취소
            reserv = check_queue.popleft()
            print('없는 번호', reserv[0], reserv[2])
            db_res = DB.reservation_cancel(reserv[0])
        else:
            # 알수 없는 에러
            reserv = check_queue.popleft()
            print('알 수 없는 에러', reserv[0], reserv[2])
            regist_queue.append((reserv[0], reserv[1] + timedelta(minutes=29)))

    while regist_queue and regist_queue[0][1] < datetime.now():
        reserv_id = regist_queue.popleft()[0]
        if DB.get_current_status(reserv_id)['currentStatus'] == 'reservwait':
            res = DB.reservation_cancel(reserv_id)
            print('auto cancel', res, reserv_id)

    Timer(30 - (time.time() - start), check_regist).start()


def run_flask():
    check_regist()
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    logger = logging.getLogger('flask')
    fomatter = logging.Formatter('[ %(levelname)s ] %(asctime)s > %(message)s')
    handler = RotatingFileHandler('log.log', maxBytes=10000, backupCount=1)
    handler.setFormatter(fomatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    flask_process = Process(target=run_flask)
    interval_alrim_send = Process(target=interval_alrim_process)
    flask_process.start()
    interval_alrim_send.start()

    flask_process.join()
    # app.run(host='0.0.0.0', debug=True)
