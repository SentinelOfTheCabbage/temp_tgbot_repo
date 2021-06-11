from phase_pattern import *
from copy import deepcopy
import re

get_rating = Phase()


def on_return(menu=None, user=None, message=None):
    msg = message.content
    pos = msg.rfind('_')
    prod_key = msg[:pos]
    rating = int(msg[pos + 1:])

    print(f'<{user.id}>: GRADES "{prod_key}" = {rating}' )
    if user.rating is None:
        user.rating = []
    user.rating.append({prod_key: rating})

    arg = ''
    user.basket = user.basket[:-1]
    if user.basket == []:
        user.basket = None
        MSG = 'NEXT'
        arg = 2
    else:
        MSG = 'CURRENT'
        arg = None
    if 0 < rating < 7:
        MSG = 'NEXT'
        arg = 1
    return user, MSG, arg


def on_call(menu=None, user=None, message=None):
    user_id = user.id
    try:
        user.order_id = user.order_id
    except Exception as e:
        user.order_id = message.content[19:]
        user.order_id = int(user.order_id)

    if  user.basket == []:
        user.basket =  menu.database.get_products_from_order(user.order_id)

    title, prod_key = user.basket[-1]
    values = list(range(1, 11)) + ['Не знаю']
    callbacks = [prod_key + '_' + str(e) for e in values[:-1]] + [prod_key+'_0']
    markup = get_rating.get_buttons(
        values, callbacks, cols=3, rb=False, bb=False)
    MSG = f'Оцените, пожалуйста, качество {title} по десятибальной шкале, где 1 - очень плохое и 10 - идеальное'
    menu.bot.send_message(user_id, MSG, reply_markup=markup)

def check_access(menu, user, message):
    if user.basket != []:
        if ((message.type == 'callback') and (re.findall('[a-z]*_[0-9]{1,2}', message.content))):
            return True
    return False


def on_undo(menu=None, user=None, message=None):
    user.basket = user.basket[:-1]
    return user


setattr(get_rating, 'on_call', on_call)
setattr(get_rating, 'check_access', check_access)
setattr(get_rating, 'on_return', on_return)
setattr(get_rating, 'on_undo', on_undo)
