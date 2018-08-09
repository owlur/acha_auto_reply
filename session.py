import time
from conversation import setting


class Session:
    def __init__(self, user_key):
        self.user_key = user_key
        self.step = 1
        self.history = []
        self.lastest = time.time()
        self.next = setting.init_response

    def receive_message(self, type, content):
        self.step += 1
        print('user_key : ',self.user_key,'\ncontent : ',content)
        if type == 'text':
            self.next = self.next.next_function(self.user_key, content)
        else:
            print('type is not text')
            self.next = setting.init_response

        return self.next.get_response()
