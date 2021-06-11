from phase_pattern import *
import re
from copy import deepcopy
service_feedback = Phase()


def on_return(menu=None, user=None, message=None):
    print(f'<{user.id}>: RATES PRODUCTS QUALITY')
    user.rating.append({'service': message.content})
    return user, 'NEXT', None


def on_call(menu=None, user=None, message=None):
    MSG = 'Что бы вы поменяли в нашем сервисе заказа Морепродуктов? (Расширение ассортимента, акции и пр)'
    values = ['Пропустить']
    callbacks = ['continue_s']
    markup = service_feedback.get_buttons(
        values, callbacks, bb=False, rb=False)
    menu.bot.send_message(user.id, MSG, reply_markup=markup)


def check_access(menu, user, message):
    if (message.type == 'message') or (message.content == 'continue_s'):
        return True
    return False


def on_undo(menu=None, user=None, message=None):
    return user

setattr(service_feedback, 'on_return', on_return)
setattr(service_feedback, 'on_call', on_call)
setattr(service_feedback, 'check_access', check_access)
setattr(service_feedback, 'on_undo', on_undo)
