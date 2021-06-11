from phase_pattern import *
from copy import deepcopy

first = Phase()


def on_return(menu=None, user=None, message=None):
    return user, None, None


def on_call(menu=None, user=None, message=None):
    user_id = user.id
    values = ['Новая поставка \u274C',
              'Обновление себестоимостей \u274C', 'Admin shop \U0001F371', 'Отчёты \U0001F4CB']

    callbacks = ['add_sup', 'update_last_orders', 'adm_shop', 'otchety']

    markup = first.get_buttons(values, callbacks, cols=2, bb=False, rb=False)
    MSG = 'Hello world!'
    menu.bot.send_message(user_id, MSG, reply_markup=markup)


def check_access(menu, user, message):
    return False


def on_undo(menu=None, user=None, message=None):
    return user


setattr(first, 'on_call', on_call)
setattr(first, 'check_access', check_access)
setattr(first, 'on_return', on_return)
setattr(first, 'on_undo', on_undo)
# del on_call, on_return, check_access
