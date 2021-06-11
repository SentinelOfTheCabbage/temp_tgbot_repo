from phase_pattern import *
import MKAD
addr = Phase()


def on_return(menu=None, user=None, message=None):
    # Что должна делать функция на действия, совершенные после on_call
    # Что делать с нажатой кнопкой/введёнными даннывми и т.п.
    if message.type == 'callback':
        user.comment = user.approx_data
    else:
        user.comment = message.content

    user_bonuses_amount = menu.database.get_bonuses(user.id)
    if user_bonuses_amount != [] and user_bonuses_amount[0][0] != 0:
        setattr(user, 'bonuses_amount', user_bonuses_amount[0][0])
        return user, 'NEXT', 1
    else:
        return user, 'NEXT', 2


def on_call(menu=None, user=None, message=None):
    menu.database.to_log(user, message, 'comment')
    # ЧТо делает функция при вызове данной фазы
    basket = user.basket

    sum_price = sum([i['price'] for i in basket])
    if user.promocode:
        sum_price *= user.discount
    # status, dost_price, coords = menu.dost.calculate_order_price(user,1)
    if user.address == 'Склад':
        status, dost_price, coords = 'OK', 0, (37.5959849, 55.6566558)
        content_text = 'Складистам салам, остальным соболезную'
    else:
        status, dost_price, coords = menu.dost.calculate_order_price(
            user.__dict__(), 3)
        content_text = ''

    if status == 'OK':
        zone_info = MKAD.is_mkad_zone(*coords)
        if zone_info is True:
            if sum_price >= 3800 or user.is_addr_free():
                delivery_price = 0
                content_text += 'Доставка бесплатная!'
            else:
                delivery_price = 200
                content_text += 'Стоимость доставки 200 руб'
        elif zone_info is False:
            if sum_price >= 8000:
                delivery_price = 0
                content_text += 'Доставка беслпатная!'
            else:
                A = dost_price - 0.06 * sum_price
                B = 0.6 * dost_price
                delivery_price = int(max(A, B))
                content_text += f'Стоимость доставки {delivery_price} руб'

    else:
        delivery_price = 0

    setattr(user, 'delivery_price', delivery_price)
    setattr(user, 'status', status)

    user_comment = menu.database.get_user_last_comment(user.id)
    markup = None
    if user_comment:
        user_comment = user_comment[0][1]
        user.approx_data = user_comment
        content_text += '\nВыберите или введите вручную комментарии к заказу'
        markup = addr.get_buttons(
            [user_comment], ['confirm_comment'], bb=False, rb=False)
    else:
        content_text += '\nКомментарри к заказу:'

    content_text += '\n(подъезд, домофон, этаж, пр. детали):'
    menu.bot.send_message(user.id, content_text, reply_markup=markup)


def check_access(menu, user, message):
    # Триггеры фазы
    if message.type == 'message':
        return True
    elif message.content == 'confirm_comment':
        return True
    else:
        return False


def on_undo(menu, user, message):
    # При использовании backbutton
    user.comment = None
    return user

setattr(addr, 'check_access', check_access)
setattr(addr, 'on_return', on_return)
setattr(addr, 'on_call', on_call)
setattr(addr, 'on_undo', on_undo)
