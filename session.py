import time
from conversation import *
from conversation import setting, initial


class Session:
    def __init__(self, user_key):
        self.user_key = user_key
        self.step = 1
        self.history = []
        self.lastest = time.time()
        self.next = initial.keyboard

    def receive_message(self, type, content):
        self.step += 1
        if type == 'text':
            for button_name in self.next.buttons:
                if button_name == content and self.next.buttons[button_name]:
                    self.next = self.next.buttons[button_name](self.user_key)
                    return self.next.get_response()
        else:
            self.next = initial.keyboard
            return setting.fallback.get_response()
