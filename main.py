from flask import Flask, send_from_directory
from flask_restful import Resource, Api, reqparse
from conversation import setting
from session import Session
from alrim import processing, send
from datetime import datetime, timedelta
import time
import DB, utils
from threading import Timer
from multiprocessing import Process

app = Flask(__name__, static_folder='page')
api = Api(app)

message_parser = reqparse.RequestParser()
message_parser.add_argument('user_key')
message_parser.add_argument('type')
message_parser.add_argument('content')

reserv_token = []
sessions = {}
session_queue = []


def interval_alrim_process():
    """
    1분 간격으로 보낼 알림이 있는지 체크
    5분 간격으로 새로운 알림 리스트 요청 -> 이때 10분치의 알림 받아옴
    """
    alrim_queue = DB.get_alrim_list(minute=10)
    five_minute_check = time.time()
    while True:
        print('one minute check')
        one_minute_check = time.time()
        if time.time() - five_minute_check > 360:
            print('five minute check')
            five_minute_check = time.time()
            alrim_queue = DB.get_alrim_list(minute=10)
            while alrim_queue and alrim_queue[0]['send_time'] < last_alrim_time:
                alrim_queue.popleft()
        now = datetime.now()

        # 알림큐가 비어있지 않고 맨 앞의 원소가 보내야할때
        while alrim_queue and alrim_queue[0]['send_time'] < now + timedelta(minutes=1):
            alrim_info = alrim_queue.popleft()
            print(send.send_interval_alrim(alrim_info['phone_number'], alrim_info['store_name'],
                                           alrim_info['person_name'],
                                           alrim_info['person_num'], alrim_info['reserv_date'],
                                           alrim_info['until_time'],
                                           alrim_info['address'], alrim_info['token']))
            last_alrim_time = alrim_info['send_time']

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
            print('알림톡 응답 수신')
            res = processing.alrim_response_parsing(sessions[user_key], content_parse[0],
                                                    '\n'.join(content_parse[2:]))
            if res:
                return res

        return sessions[user_key].receive_message(type, content)


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


class ReservRegist(Resource):
    def post(self):
        args = reserv_parser.parse_args()
        dt = datetime.fromtimestamp(int(args['reservDate']) / 1000)
        args['reservDate'] = utils.datetime2str(dt)
        processing.reserv_regist(args['phoneNumber'], args['storeName'], args['reservName'], args['reservNumber'],
                                 args['reservDate'], args['reservToken'])
        print(args)


class PrivacyPolicy(Resource):
    def get(self):
        return send_from_directory('page', 'PrivacyPolicy.html')


""""@app.before_first_request
def initialize():
    global alrim_queue
    alrim_queue = DB.get_today_alrim_list()
    for alrim_info in alrim_queue:
        print(alrim_info)
    Timer(0, check_alrim_queue).start()
"""

api.add_resource(Keyboard, '/keyboard')
api.add_resource(Message, '/message')
api.add_resource(Friend, '/friend')
api.add_resource(FriendDelete, '/friend/<user_key>')
api.add_resource(ChatRoom, '/chat_room/<user_key>')
api.add_resource(ReservRegist, '/reserv/regist')
api.add_resource(PrivacyPolicy, '/PrivacyPolicy')

if __name__ == '__main__':
    flask_process = Process(target=app.run, kwargs={'host': '0.0.0.0'})
    interval_alrim_send = Process(target=interval_alrim_process)
    flask_process.start()
    interval_alrim_send.start()

    flask_process.join()
    # app.run(host='0.0.0.0', debug=True)
