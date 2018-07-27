from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from conversation import *
from conversation import initial
from session import Session
from response import Response

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('user_key')
parser.add_argument('type')
parser.add_argument('content')


sessions = {}


class Keyboard(Resource):
    def get(self):
        resp = initial.keyboard
        print(resp.buttons.keys())
        return {'type': resp.type, 'buttons': list(resp.buttons.keys())}


class Message(Resource):
    def post(self):
        # 세션 구분
        # 다음 함수 호출


        print('test')
        args = parser.parse_args()

        user_key = args['user_key']
        print('test2')
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
        args = parser.parse_args()
        user_key = args['user_key']
        return {'message': user_key}


class FriendDelete(Resource):
    def delete(self, user_key):
        return {'message': user_key}


class ChatRoom(Resource):
    def delete(self,user_key):
        return {'message': user_key}


api.add_resource(Keyboard, '/keyboard')
api.add_resource(Message, '/message')
api.add_resource(Friend,'/friend')
api.add_resource(FriendDelete,'/friend/<user_key>')
api.add_resource(ChatRoom,'/chat_room/<user_key>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)