from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from conversation import setting
from session import Session
import alrim

app = Flask(__name__)
api = Api(app)

message_parser = reqparse.RequestParser()
message_parser.add_argument('user_key')
message_parser.add_argument('type')
message_parser.add_argument('content')


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


        print('test')
        args = message_parser.parse_args()

        user_key = args['user_key']
        type = args['type']
        content = args['content']

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


alrim_parser = reqparse.RequestParser()
alrim_parser.add_argument('phone_number')
alrim_parser.add_argument('store_name')
alrim_parser.add_argument('person_num')
alrim_parser.add_argument('date')


class SendAlrim(Resource):
    def post(self):
        alrim_parser.parse_args()
        alrim.send

api.add_resource(Keyboard, '/keyboard')
api.add_resource(Message, '/message')
api.add_resource(Friend,'/friend')
api.add_resource(FriendDelete,'/friend/<user_key>')
api.add_resource(ChatRoom,'/chat_room/<user_key>')
api.add_resource(SendAlrim,'/send_alrim')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)