from phase_pattern import *
import MKAD
from datetime import datetime
finish = Phase()


def on_return(menu=None, user=None, message=None):
    # Что должна делать функция на действия, совершенные после on_call
    # Что делать с нажатой кнопкой/введёнными даннывми и т.п.
    return user, None, None


def on_call(menu=None, user=None, message=None):
    # menu.database.to_log(user, message, 'end')
    basket = user.basket
    user_info = user.__str__()

    sum_price = sum([i['price'] for i in user.basket])
    res_price = sum_price

    # if not(user.id in menu.testers_id_list):
    #     for elem in menu.admin_list:
    #         menu.bot.send_message(elem, user_info)

    p_keys = {}
    for elem in menu.products:
        p_keys[menu.products[elem]['key']] = menu.products[elem]['title']

    markup = finish.get_buttons(
        ['Начать заново'], ['start'], bb=False, rb=False, fb=True)

    content_text = f'Поставка\n'

    for elem in user.basket:
        content_text += f'{elem["title"]} [x{elem["amount"]}] - {elem["price"]} руб\n'

    keys = [e['key'] for e in basket]

    menu.bot.send_message(user.id, content_text, reply_markup=markup)
    print(user.basket)
    menu.database.create_supply(user.basket)

    del menu.current_users[user.id]


def check_access(menu, user, message):
    return False


def on_undo(menu, user, message):
    return user

setattr(finish, 'check_access', check_access)
setattr(finish, 'on_return', on_return)
setattr(finish, 'on_call', on_call)
setattr(finish, 'on_undo', on_undo)
