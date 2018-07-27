from response import Keyboard
from conversation import setting

keyboard = Keyboard(setting.default_keyboard)
for command in setting.commands:
    keyboard.set_function(command, setting.commands[command])
