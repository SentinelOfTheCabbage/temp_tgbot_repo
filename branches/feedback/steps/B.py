from phase_pattern import *
import re
from copy import deepcopy
feedback_comment = Phase()


def on_return(menu=None, user=None, message=None):
    user.rating[-1]['comment']= message.content
    if message.type == 'callback':
        print(f'<{user.id}>: SKIPPED COMMENT PHASE' )
    else:
        print(f'<{user.id}>: JUST WROTE COMMENT')

    # user.basket = user.basket[:-1]
    if (user.basket == []) or (user.basket == None):
        user.basket = None
        return user, 'NEXT', None
    else:
        return user, 'PREVIOUS', None


def on_call(menu=None, user=None, message=None):
    MSG = 'Опишите, пожалуйста, что именно вас не устроило в качесте продукции?'
    values = ['Пропустить']
    callbacks = ['continue_q']
    markup = feedback_comment.get_buttons(
        values, callbacks, bb=False, rb=False)
    menu.bot.send_message(user.id, MSG, reply_markup=markup)


def check_access(menu, user, message):
    if (message.type == 'message') or (message.content == 'continue_q'):
        return True
    return False


def on_undo(menu=None, user=None, message=None):
    return user

setattr(feedback_comment, 'on_return', on_return)
setattr(feedback_comment, 'on_call', on_call)
setattr(feedback_comment, 'check_access', check_access)
setattr(feedback_comment, 'on_undo', on_undo)
