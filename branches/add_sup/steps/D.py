from phase_pattern import *
from copy import deepcopy
fyr = Phase()


def on_return(menu=None, user=None, message=None):
    common_button = 'create_supply'
    keys = list(menu.products.keys())
    key = message.content
    if message.content == common_button:
        msg = 'NEXT'
        arg = None
    elif key in keys:
        user.basket.append(deepcopy(menu.products[key]))
        msg = 'PREVIOUS'
        arg = 2
    return user, msg, arg


def on_call(menu=None, user=None, message=None):
    # menu.database.to_log(user, message, 'submenu')
    MSG = 'Что ещё?'
    user_id = user.id

    keys = list(menu.products.keys())
    values = [menu.products[key]['title'] for key in keys]
    callbacks = list(keys)

    markup = fyr.get_buttons(values, callbacks, cols=2, bb=False, rb=False)
    markup.add(types.InlineKeyboardButton(
        text='Создать поставку', callback_data='create_supply'))
    markup.add(types.InlineKeyboardButton(
        text='Начать заново', callback_data='restart'))

    menu.bot.send_message(user_id, MSG, reply_markup=markup)


def check_access(menu, user, message):
    keys = list(menu.products.keys()) + ['create_supply', 'restart']
    if message.type == 'callback' and message.content in keys:
        return True
    else:
        return False


def on_undo(menu, user, message):
    # При использовании backbutton
    return user


setattr(fyr, 'check_access', check_access)
setattr(fyr, 'on_return', on_return)
setattr(fyr, 'on_call', on_call)
setattr(fyr, 'on_undo', on_undo)
