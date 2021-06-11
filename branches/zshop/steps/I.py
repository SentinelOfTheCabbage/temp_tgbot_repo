from phase_pattern import *
import MKAD
set_bonuses = Phase()


def on_return(menu=None, user=None, message=None):
    # Что должна делать функция на действия, совершенные после on_call
    # Что делать с нажатой кнопкой/введёнными даннывми и т.п.
    if message.type == 'callback':
        result_amonut = int(message.content[7:])
        setattr(user, 'pay_by_bonuses', result_amonut)
    else:
        msg_nums = ''.join([i for i in message.content if i in '1234567890'])
        input_bonuses_amount = int(msg_nums)

        sum_price = sum([i['price'] for i in user.basket])
        max_value = min(sum_price, user.bonuses_amount)

        result_amonut = min(input_bonuses_amount, max_value)

        setattr(user, 'pay_by_bonuses', result_amonut)

    total_price = sum([i['price'] for i in user.basket]) + user.delivery_price
    MSG = f'Итоговая стоимость заказа {total_price - result_amonut}руб.'
    menu.bot.send_message(user.id, MSG)
    return user, 'NEXT', None


def on_call(menu=None, user=None, message=None):
    menu.database.to_log(user, message, 'use_bonus')
    # ЧТо делает функция при вызове данной фазы

    sum_price = sum([i['price'] for i in user.basket]) * \
        user.discount + user.delivery_price

    MSG = f'Итоговая стоимость заказа {sum_price}руб. На вашем бонусном счете {user.bonuses_amount} баллов, сколько баллов списать? (можете ввести вручную)'

    button_content = min(user.bonuses_amount, sum_price)
    values = [str(button_content)]
    callbacks = ['maxval_' + str(button_content)]

    markup = set_bonuses.get_buttons(values, callbacks, bb=False)
    menu.bot.send_message(user.id, MSG, reply_markup=markup)


def check_access(menu, user, message):
    if message.type == 'message':
        msg_nums = ''.join([i for i in message.content if i in '1234567890'])
        if len(msg_nums) > 0:
            return True
        return False
    elif 'maxval_' in message.content:
        return True
    else:
        return False


def on_undo(menu, user, message):
    # При использовании backbutton
    user.comment = None
    return user

setattr(set_bonuses, 'check_access', check_access)
setattr(set_bonuses, 'on_return', on_return)
setattr(set_bonuses, 'on_call', on_call)
setattr(set_bonuses, 'on_undo', on_undo)
