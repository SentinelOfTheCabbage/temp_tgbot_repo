from phase_pattern import *

rea = Phase()


def on_return(menu=None, user=None, message=None):
    # Что должна делать функция на действия, совершенные после on_call
    # Что делать с нажатой кнопкой/введёнными даннывми и т.п.
    if message.type == 'callback':
        user.address = user.approx_data
    else:
        user.address = message.content
    return user, 'NEXT', None


def on_call(menu=None, user=None, message=None):
    # ЧТо делает функция при вызове данной фазы
    menu.database.to_log(user, message, 'address')
    MSG = f'Вы ввели дату {user.delivery_date}'

    prod_prices = [e['price'] for e in user.basket]
    result_price = sum(prod_prices)
    if user.promocode:
        result_price *= user.discount

    if result_price >= 8000:
        MSG += '\nСтоимость доставки - бесплатно'

    elif result_price >= 3800:
        MSG += '\nСтоимость доставки внутри МКАД - бесплатно'
        MSG += '\nМО - индивидуальный расчёт'
    else:
        MSG += '\nСтоимость доставки на дом внутри МКАД - 200р.'
        MSG += '\nМО - индивидуальный расчёт'

    user_address = menu.database.get_user_last_address(user.id)
    markup = None
    if user_address:
        user_address = user_address[0][1]
        user.approx_data = user_address
        MSG += '\nВыберите или введите вручную ваш адрес\n'
        markup = rea.get_buttons(
            [user_address], ['confirm_address'], bb=False, rb=False)
    else:
        MSG += '\nВведите ваш адрес\n'
    MSG += '(ТОЛЬКО нас. пункт, улица и дом):'
    menu.bot.send_message(user.id, MSG, reply_markup=markup)


def check_access(menu, user, message):
    # Триггеры фазы
    if message.type == 'message':
        return True
    elif message.content == 'confirm_address':
        return True
    else:
        return False


def on_undo(menu, user, message):
    # При использовании backbutton
    user.address = None
    return user

setattr(rea, 'check_access', check_access)
setattr(rea, 'on_return', on_return)
setattr(rea, 'on_call', on_call)
setattr(rea, 'on_undo', on_undo)
