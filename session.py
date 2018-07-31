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
            for button_name in self.next.buttons:
                if button_name == content:
                    if self.next.buttons[button_name]:
                        self.next = self.next.buttons[button_name](self.user_key)
                        break
                    else:
                        self.next = setting.init_response
            else:
                self.next = setting.init_response
        else:
            self.next = setting.init_response

        return self.next.get_response()
