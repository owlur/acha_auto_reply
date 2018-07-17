import time
import conversation


class Session:
    def __init__(self, user_key):
        self.user_key = user_key
        self.step= 1
        self.history = []
        self.lastest = time.time()
        self.next = conversation.init

    def recieve_message(self, type, content):
        self.step += 1
        for i in self.next:
            if i[:2] == (type, content):
                callback = i[2]
                break
        else:
            self.next = conversation.init
            return conversation.fallback

