from phase_pattern import *
from copy import deepcopy

bonuses_main_page = Phase()


def on_return(menu=None, user=None, message=None):
    return user, 'NEXT', None

# @bonuses_main_page.action_logger
def on_call(menu=None, user=None, message=None):
    menu.database.to_log(user, message,'bonuses')
    user_id = user.id

    values = ['Получить промо-код \U0001F3C6']
    callbacks = ['get_promocode']

    markup = bonuses_main_page.get_buttons(values, callbacks, cols=1, bb=False)
    bonuses = menu.database.get_bonuses(user_id)
    if not bonuses:
        bonuses = 0
    else:
        print(bonuses)
        bonuses = int(bonuses[0][0])

    MSG = f'На вашем балансе сейчас {bonuses} бонусов'
    if bonuses > 0:
        MSG += ', вы можете использовать их введя свой личный промокод'
    menu.bot.send_message(user_id, MSG, reply_markup=markup)


def check_access(menu, user,message):
    if (message.type == 'callback') and (message.content == 'get_promocode'):
        return True
    else:
        return False

def on_undo(menu=None,user=None,message=None):
    user.basket = user.basket[:-1]
    return user


setattr(bonuses_main_page, 'on_call', on_call)
setattr(bonuses_main_page, 'check_access', check_access)
setattr(bonuses_main_page, 'on_return',on_return)
setattr(bonuses_main_page, 'on_undo', on_undo)
# del on_call, on_return, check_access
