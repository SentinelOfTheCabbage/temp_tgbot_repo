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
    return user, 'NEXT', None


def on_call(menu=None, user=None, message=None):
    menu.database.to_log(user, message, 'comment')
    # ЧТо делает функция при вызове данной фазы
    basket = user.basket

    sum_price = sum([i['price'] for i in basket])

    # status, dost_price, coords = menu.dost.calculate_order_price(user,1)
    if user.address == 'Склад':
        status, dost_price, coords = 'OK', 0, (37.5959849, 55.6566558)
        content_text = 'Складистам салам, остальным соболезную\n'
    else:
        status, dost_price, coords = menu.dost.calculate_order_price(
            user.__dict__(), 3)
        content_text = ''

    if status == 'OK':
        content_text += f'Стоимость доставки {dost_price} руб'
    else:
        content_text += 'Что-то пошло криво =/ Мб адрес косой?'

    markup = None

    user_comment = menu.database.get_user_last_comment(user.id)
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

    user.delivery_price = dost_price


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
