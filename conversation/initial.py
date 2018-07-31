from response import Response, Keyboard
from conversation import setting

keyboard = Keyboard(setting.default_keyboard)
for command in setting.commands:
    keyboard.set_function(command, setting.commands[command])

init_response = Response('아차 입니다\n 무엇을 도와 드릴까요?', keyboard_buttons=setting.default_keyboard)
for command in setting.commands:
    init_response.set_function(command, setting.commands[command])