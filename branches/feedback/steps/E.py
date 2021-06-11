from phase_pattern import *
import re
from copy import deepcopy
select_pack_size = Phase()


def on_return(menu=None, user=None, message=None):
    print('E onret')
    return user, None, None


def on_call(menu=None, user=None, message=None):
    MSG = 'Спасибо, что помогаете нам становиться лучше!'
    markup = select_pack_size.get_buttons([],[],rb=True,bb=False)
    menu.bot.send_message(user.id, MSG, reply_markup=markup)

    product_keys = [key for key in menu.products]
    for admin in menu.admin_list:
        try:
            MSG = 'Обратная связь:\n'
            MSG += f'Клиент: {user.id}\n'
            for feedback in user.rating:
                for key in feedback:
                    if key == 'comment':
                        MSG += ' -'
                    if key in product_keys:
                        MSG += f'{menu.products[key]["title"]} : {feedback[key]}\n'
                    else:
                        MSG += f'{key}: {feedback[key]}\n'
            menu.bot.send_message(admin,MSG)
        except Exception as e:
            menu.bot.send_message(295932236,e)
    try:
        menu.database.update_order_feedback_status(user.order_id)
    except Exception as e:
        menu.bot.send_message(295932236,e)
    del menu.current_users[user.id]

def check_access(menu, user, message):
    return False


def on_undo(menu=None,user=None,message=None):
    return user

setattr(select_pack_size, 'on_return', on_return)
setattr(select_pack_size, 'on_call', on_call)
setattr(select_pack_size, 'check_access', check_access)
setattr(select_pack_size, 'on_undo', on_undo)
