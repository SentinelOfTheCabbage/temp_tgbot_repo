from phase_pattern import *
import MKAD
finish = Phase()


def on_return(menu=None, user=None, message=None):
    # Что должна делать функция на действия, совершенные после on_call
    # Что делать с нажатой кнопкой/введёнными даннывми и т.п.
    return user, None, None


def on_call(menu=None, user=None, message=None):
    menu.database.to_log(user, message, 'end')
    # ЧТо делает функция при вызове данной фазы
    basket = user.basket
    user_info = user.__str__()

    sum_price = sum([i['price'] for i in user.basket])
    total_price_str = f'\nTotal_price = {sum_price}'
    if not(user.id in menu.testers_id_list):
        for elem in menu.admin_list:
            menu.bot.send_message(elem, user_info + total_price_str)

    p_keys = {}
    for elem in menu.products:
        p_keys[menu.products[elem]['key']] = menu.products[elem]['title']

    sum_price = sum([i['price'] for i in user.basket])

    markup = finish.get_buttons(
        ['Начать заново'], ['start'], bb=False, rb=False, fb=True)

    content_text = f'Спасибо, {user.name}, ваш заказ принят\n'
    content_text += f'Ваш номер: {user.phone}\n'
    content_text += f'Ваш заказ:\n'

    for elem in user.basket:
        content_text += f'{elem["title"]} [x{elem["amount"]}] - {elem["price"]} руб\n'
    content_text += f'\nЗаказ будет доставлен по адресу {user.address}\n'

    hours = user.delivery_time.replace('to', '-')
    content_text += '{} в {} часов\n'.format(user.delivery_date, hours)

    if user.address == 'Склад':
        status, dost_price = 'OK', 0
        content_text += 'Склад\n'
    else:
        status, dost_price, coords = menu.dost.calculate_order_price(
            user.__dict__, 3)

    # delivery_price = dost_price

    content_text += f'\nОбщая стоимость заказа c учётом доставки составит {sum_price + dost_price} руб. (доставка {dost_price} руб.)'

    keys = [e['key'] for e in basket]

    if 'fish_forel' in keys:
        content_text = content_text.replace(
            'Общая стоимость заказа', 'Приблизительная стоимость заказа')
        content_text += '\nДля оплаты воспользуйтесь банковским переводом по номеру телефона: +7 (968) 719-59-22 (Сбербанк, Тиньков, Альфа)'

    menu.bot.send_message(user.id, content_text, reply_markup=markup)

    user.delivery_cost = user.delivery_price
    menu.database.on_finish(user.__dict__())

    order_id = menu.database.get_last_order_id() + 1
    if not (user.id in menu.testers_id_list):
        for elem in menu.admin_list:
            menu.bot.send_message(elem, user_info)
        send_adm_message(menu, user.__dict__(), order_id)

    for product in user.basket:
        menu.products[product['key']][
            'in_stock'] -= product['amount'] * product['pack_size']
        if menu.products[product['key']]['in_stock'] < 0:
            menu.products[product['key']]['in_stock'] = 0

    if not (user.id in menu.testers_id_list):
        for elem in menu.admin_list:
            menu.bot.send_message(elem, f'Dostavista status {status}')
    del menu.current_users[user.id]


def check_access(menu, user, message):
    # Триггеры фазы
    return False


def on_undo(menu, user, message):
    # При использовании backbutton
    return user


def send_adm_message(menu, user, order_id):
    name = user['name']
    phone = user['phone']
    basket = user['basket']
    address = user['address']
    time = user['delivery_time']
    date = user['delivery_date']
    tmp = time.find('to')
    time = int(time[:tmp])

    p_keys = {}
    p_size = {}
    for elem in menu.products:
        p_keys[elem] = menu.products[elem]['title']
        p_size[elem] = menu.products[elem]['pack_size']

    msg = f'Заказ №{order_id}:\n'
    for elem in basket:
        if 'pack' in elem['key']:
            size = elem['amount']
        elif 'prod' in elem['key']:
            size = round(elem['amount'] / p_size[elem['key']])
        elif 'fish' in elem['key']:
            size = elem['amount']

        msg += f'{p_keys[elem["key"]]} [x{elem["amount"]}] {size} по {1000*p_size[elem["key"]]}\n'

    msg += f'\nАдрес доставки: {address}\n'
    msg += f'Курьер прибудет {date} с {time-1}:30 до {time}'

    for id in menu.admin_list:
        menu.bot.send_message(id, msg)


setattr(finish, 'check_access', check_access)
setattr(finish, 'on_return', on_return)
setattr(finish, 'on_call', on_call)
setattr(finish, 'on_undo', on_undo)
