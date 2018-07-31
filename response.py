import collections


class Keyboard:
    def __init__(self, keyboard_buttons=False):
        self.buttons = collections.OrderedDict()
        if type(keyboard_buttons) == list:
            self.type = 'buttons'
            for button in keyboard_buttons:
                self.buttons[button] = None
        else:
            self.type = 'text'

    def set_function(self, button, function):
        self.buttons[button] = function

    def get_function(self, button):
        return self.buttons[button]


class Keyboard:
    def __init__(self, keyboard_buttons=False):
        self.buttons = collections.OrderedDict()
        if type(keyboard_buttons) == list:
            self.type = 'buttons'
        else:
            self.type = 'text'

    def set_function(self,  function):
        self.next_function = function

    def get_function(self):
        return self.next_function

class Response(Keyboard):
    def __init__(self, message, photo=False, message_button=False, keyboard_buttons=False):
        """
        :param message: 전송 메시지
        :param photo: 전송 사진 url, width, height 순으로 iterator로 넘길것
        :param message_button: [(label1, url1), (label2, url2)...]로 넘길것
        :param keyboard_buttons: list로 넘기면 keyboard type을 buttons로 전송
        """

        super(Response, self).__init__(keyboard_buttons=keyboard_buttons)
        self.message = message

        # 예외 처리 작성할것
        self.photo = photo
        self.message_button = message_button

    # 바로 전송할 수 있도록 만들것
    def get_response(self):
        resp = {'message': {'text': self.message}, 'keyboard': {'type': self.type}}

        if self.type == 'buttons':
            resp['keyboard']['buttons'] = list(self.buttons.keys())

        if self.photo:
            resp['message']['photo'] = {'url': self.photo[0], 'width': self.photo[1], 'height': self.photo[2]}

        if self.message_button:
            resp['message']['message_button'] = {'label': self.message_button[0], 'url': self.message_button[1]}

        print(resp)
        print('\n\n')
        resp
        return resp

    def __str__(self):
        return str(self.get_response())
