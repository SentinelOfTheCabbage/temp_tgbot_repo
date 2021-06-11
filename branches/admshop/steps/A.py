from phase_pattern import *
from copy       import deepcopy

first = Phase()


def on_return(menu=None, user=None, message=None):
    key = message.content
    user.basket.append(deepcopy(menu.products[key]))
    return user, 'NEXT', None

def on_call(menu=None, user=None, message=None):
    menu.database.to_log(user, message,'start')
    user_id = user.id
    products = menu.products
    keys = products.keys()
    values = [products[key]['title'] for key in keys]

    callbacks = [key for key in keys]

    markup = first.get_buttons(values, callbacks, cols=2, bb=False)
    MSG = 'SECRET SHOP'
    menu.bot.send_message(user_id, MSG, reply_markup=markup)


def check_access(menu, user,message):
    if (message.type == 'callback') and (message.content in menu.products):
        return True
    else:
        return False

def on_undo(menu=None,user=None,message=None):
    user.basket = user.basket[:-1]
    return user


setattr(first, 'on_call', on_call)
setattr(first, 'check_access', check_access)
setattr(first, 'on_return',on_return)
setattr(first, 'on_undo', on_undo)
# del on_call, on_return, check_access
