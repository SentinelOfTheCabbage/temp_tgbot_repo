from phase_pattern import *
import MKAD
from datetime import datetime
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
    if user.promocode:
        sum_price *= user.discount
        if sum_price > 2000:
            menu.database.give_revard_by_promo(user.promocode)
            menu.database.update_uses(user.id)

    if user.pay_by_bonuses:
        res_price = sum_price - int(user.pay_by_bonuses)
    else:
        res_price = sum_price

    # total_price_str = f'\nTotal_price = {sum_price} ({res_price} + bonuses)'
    # if not(user.id in menu.testers_id_list):
    #     for elem in menu.admin_list:
    #         menu.bot.send_message(elem, user_info + total_price_str)

    p_keys = {}
    for elem in menu.products:
        p_keys[menu.products[elem]['key']] = menu.products[elem]['title']

    markup = finish.get_buttons(
        ['Начать заново'], ['start'], bb=False, rb=False, fb=True)

    content_text = f'Спасибо, {user.name}, ваш заказ принят\n'
    content_text += f'Ваш номер: {user.phone}\n'
    content_text += f'Ваш заказ:\n'

    for elem in user.basket:
        content_text += f'{elem["title"]} [x{elem["amount"]}] - {elem["price"]} руб\n'

    if user.promocode:
        content_text += f"~Скидка по промокоду - {int(sum_price/user.discount*(1-user.discount))} рублей~\n"
    if user.pay_by_bonuses and user.pay_by_bonuses > 0:
        content_text += f'~Списано {user.pay_by_bonuses} баллов~\n'

    content_text += f'\nЗаказ будет доставлен по адресу {user.address} '

    hours = user.delivery_time.replace('to', '-')
    content_text += '{} в {} часов\n'.format(user.delivery_date, hours)

    order_id = menu.database.get_last_order_id() + 1
    if user.address == 'Склад':
        status, dost_price, coords = 'OK', 0, (37.5959849, 55.6566558)
        content_text += '(Склад)'
    else:
        status, delivery_cost, coords = menu.dost.create_order(
            user.__dict__(), order_id)

    # if user.bonuses:
    #     content_text += f'С вашего баланса будет списано {user.bonuses} бонусов (={user.bonuses} руб).'

    delivery_price = 0
    if user.status == 'OK':
        if MKAD.is_mkad_zone(*coords):
            if sum_price >= 3800 or user.is_addr_free():
                content_text += f'\nОбщая стоимость заказа составит {res_price} руб.  Доставка бесплатная!'
            else:
                content_text += f'\nОбщая стоимость заказа с учётом доставки составит {res_price + 200} руб. (доставка 200 руб.)'
        else:
            if sum_price >= 8000:
                content_text += f'\nОбщая стоимость заказа составит {res_price} руб. Доставка беслпатная'
            else:
                content_text += f'\nОбщая стоимость заказа c учётом доставки составит {res_price + user.delivery_price} руб. (доставка {user.delivery_price} руб.)'
    else:
        content_text += f'\nОбщая стоимость заказа составит {sum_price} руб. + доставка'
    keys = [e['key'] for e in basket]

    if 'fish_forel' in keys:
        content_text = content_text.replace(
            'Общая стоимость заказа', 'Приблизительная стоимость заказа')
        content_text += '\nПосле доставки мы вышлем вам фактический вес рыбы и общую стоимость заказа.\nОплата производится после доставки - банковским переводом по номеру телефона (не курьеру):'
        # if user.referal_id == 442774493:
        #     content_text += '+7 (965) 410-12-59 (Сбербанк, Тиньков)'
        # else:
        content_text += '+7 (968) 719-59-22 (Сбербанк, Тиньков, Альфа)'
    else:
        if user.referal_id == 442774493:
            content_text += '\nОплата производится после доставки - банковским переводом по номеру телефона (не курьеру): +7 (965) 410-12-59 (Сбербанк, Тиньков)'
        else:
            content_text += '\nОплата производится после доставки - банковским переводом по номеру телефона (не курьеру): +7 (968) 719-59-22 (Сбербанк, Тиньков, Альфа)'
    menu.bot.send_message(user.id, content_text, reply_markup=markup)

    # if user.address != 'Склад':
    #     user.delivery_cost = delivery_cost
    #     user.delivery_price = delivery_price
    # else:
    #     user.delivery_price = 0
    #     user.delivery_cost = 0
    menu.database.on_finish(user.__dict__())

    if not(user.id in menu.testers_id_list):
        for elem in menu.admin_list:
            menu.bot.send_message(elem, user_info)
        send_adm_message(menu, user.__dict__(), order_id)

    print(f'[{user.id}]: DOST_STATUS {status}')
    if status == 'OK':
        for product in user.basket:
            menu.products[product['key']][
                'in_stock'] -= product['amount'] * product['pack_size']
            if menu.products[product['key']]['in_stock'] < 0:
                menu.products[product['key']]['in_stock'] = 0
    #         product_key = product['key']
    #         product_weight = product['amount']*product['pack_size']
    #         menu.database.update_stock(product_key,product_weight,user)

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

    if user['delivery_date'] == datetime.now().strftime('%d.%m.%y'):
        BORIS_ID = 1488670156
        menu.bot.send_message(BORIS_ID, msg)

setattr(finish, 'check_access', check_access)
setattr(finish, 'on_return', on_return)
setattr(finish, 'on_call', on_call)
setattr(finish, 'on_undo', on_undo)
