from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from conversation import setting
from session import Session
from alrim import processing
import time

app = Flask(__name__)
api = Api(app)

message_parser = reqparse.RequestParser()
message_parser.add_argument('user_key')
message_parser.add_argument('type')
message_parser.add_argument('content')

reserv_token = []
sessions = {}


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

        content_parse = content.split('\n')
        if len(content_parse) > 2 and not content_parse[1] and content_parse[0] in setting.alrim_keyword:
            print('알림톡 응답 수신')
            processing.parse_initial_reservation_alrim('\n'.join(content_parse[2:]))

        if sessions.get(user_key):
            return sessions[user_key].receive_message(type, content)
        else:
            sessions[user_key] = Session(user_key)
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
    def delete(self,user_key):
        return {'message': user_key}


reserv_parser = reqparse.RequestParser()
reserv_parser.add_argument('phoneNumber')
reserv_parser.add_argument('storeName')
reserv_parser.add_argument('reservName')
reserv_parser.add_argument('reservNumber')
reserv_parser.add_argument('reservDate')
reserv_parser.add_argument('reservToken')


class SendAlrim(Resource):
    def post(self):
        reserv_parser.parse_args()


class ReservRegist(Resource):
    def post(self):
        args = reserv_parser.parse_args()
        ts = time.gmtime(int(args['reservDate']))
        args['reservDate'] = '%d월 %d일 %d시 %d분' % (ts.tm_month, ts.tm_mday, ts.tm_hour, ts.tm_min)
        processing.reserv_regist(args['phoneNumber'],args['storeName'], args['reservName'], args['reservNumber'], args['reservDate'], args['reservToken'])
        print(args)



api.add_resource(Keyboard, '/keyboard')
api.add_resource(Message, '/message')
api.add_resource(Friend,'/friend')
api.add_resource(FriendDelete,'/friend/<user_key>')
api.add_resource(ChatRoom,'/chat_room/<user_key>')
api.add_resource(SendAlrim,'/send_alrim')
api.add_resource(ReservRegist,'/reserv/regist')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)