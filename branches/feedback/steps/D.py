from phase_pattern import *
import re
from copy import deepcopy
bot_feedback = Phase()


def on_return(menu=None, user=None, message=None):
    print(f'<{user.id}>: RATES SERVICE QUALITY')
    user.rating.append({'bot': message.content})
    return user, 'NEXT', None


def on_call(menu=None, user=None, message=None):
    MSG = 'Что бы вы поменяли в нашем чат-боте? (способ оплаты, автоввод данных и пр)'
    values = ['Пропустить']
    callbacks = ['continue_b']
    markup = bot_feedback.get_buttons(
        values, callbacks, bb=False, rb=False)
    menu.bot.send_message(user.id, MSG, reply_markup=markup)


def check_access(menu, user, message):
    if (message.type == 'message') or (message.content == 'continue_b'):
        return True
    return False


def on_undo(menu=None, user=None, message=None):
    return user

setattr(bot_feedback, 'on_return', on_return)
setattr(bot_feedback, 'on_call', on_call)
setattr(bot_feedback, 'check_access', check_access)
setattr(bot_feedback, 'on_undo', on_undo)
