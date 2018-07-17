class Keyboard:
    def __init__(self, keyboard_buttons=False):
        if type(keyboard_buttons) == list:
            self.type = 'buttons'
            self.keyboard_buttons = keyboard_buttons
            self.function = [0 for i in range(len(keyboard_buttons))]
        else:
            self.type = 'text'

    def set_function(self, button_idx, function):
        self.function[button_idx] = function

    def get_function(self, button_idx):
        return self.function[button_idx]


class Response(Keyboard):
    def __init__(self, message, photo=False, message_button=False, keyboard_buttons=False):
        """
        :param message: 전송 메시지
        :param photo: 전송 사진 url, width, height 순으로 iterator로 넘길것
        :param message_button: [(label1, url1), (label2, url2)...]로 넘길것
        :param keyboard_buttons: list로 넘기면 keyboard type을 buttons로 전송
        """

        super.__init__(self, keyboard_buttons)
        self.message = message


        # 예외 처리 작성할것
        self.photo = photo
        self.message_button = message_button
