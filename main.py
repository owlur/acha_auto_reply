from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import conversation


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('user_key')


class Keyboard(Resource):
    def get(self):
        resp = conversation.init
        return {'type': resp.type, 'buttons': resp.keyboard_buttons}


class Message(Resource):
    def post(self):
        user_key = request.form['user_key']
        type = request.form['type']
        content = request.form['content']
        return {'message' : content}


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