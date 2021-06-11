from phase_pattern import *
import re
from copy import deepcopy
get_promocode_page = Phase()


def on_return(menu=None, user=None, message=None):
    return user, 'NEXT', None


def on_call(menu=None, user=None, message=None):
    menu.database.to_log(user, message, 'get_promocode')

    def generate_code(length=8):
        import random
        alphabet = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ'
        pwd = ''
        for i in range (length):
            char = alphabet[random.randint(0,len(alphabet)-1)]
            pwd += char

        del random
        return pwd

    bonus_code = menu.database.get_user_bonus_code(user.id)

    if not bonus_code:
        while True:
            bonus_code = generate_code()
            if not menu.database.is_bonus_code_existing(bonus_code,user.id):
                break
        menu.database.create_bonus_code(user.id,bonus_code)
    else:
        bonus_code = bonus_code[0][0]

    MSG = f'Ваш промокод:'
    menu.bot.send_message(user.id, MSG)
    menu.bot.send_message(user.id,bonus_code)
    del menu.current_users[user.id]


def check_access(menu, user, message):
    if message.type == 'callback':
        pattern = '[0-9]{1,}'
        if len(re.findall(pattern, message.content)) > 0:
            return True
    elif message.type == 'message':
        pattern = '[0-9]{1,}[,.]{0,}[0-9]*.*[кгршт]{0,2}'
        if len(re.findall(pattern, message.content)) > 0:
            return True
    return False


def on_undo(menu=None, user=None, message=None):
    key = user.basket[-1]['key']
    user.basket[-1]['amount'] = None
    user.basket[-1]['price'] = menu.products[key]['price']
    return user

setattr(get_promocode_page, 'on_return', on_return)
setattr(get_promocode_page, 'on_call', on_call)
setattr(get_promocode_page, 'check_access', check_access)
setattr(get_promocode_page, 'on_undo', on_undo)
