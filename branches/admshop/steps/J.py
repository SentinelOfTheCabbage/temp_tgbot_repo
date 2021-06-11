from phase_pattern import *

phone = Phase()


def on_return(menu=None, user=None, message=None):
    # Что должна делать функция на действия, совершенные после on_call
    # Что делать с нажатой кнопкой/введёнными даннывми и т.п.
    if message.type == 'callback':
        user.phone = user.approx_data
    else:
        user.phone = message.content
    return user, 'NEXT', None


def on_call(menu=None, user=None, message=None):
    menu.database.to_log(user, message,'phone')
    user_phone = menu.database.get_user_last_phone(user.id)
    markup = None
    if user_phone:
        user_phone = user_phone[0][1]
        user.approx_data = user_phone
        MSG = 'Выберите или введите вручную ваш номер телефона'
        markup = phone.get_buttons([user_phone],['confirm_number'], bb=False,rb=False)
    else:
        MSG = 'Введите ваш номер телефона'
    menu.bot.send_message(user.id, MSG,reply_markup=markup)


def check_access(menu, user, message):
    # Триггеры фазы
    if message.type == 'message':
        return True
    elif message.content == 'confirm_number':
        return True
    else:
        return False


def on_undo(menu, user, message):
    # При использовании backbutton
    user.phone = None
    return user

setattr(phone, 'check_access', check_access)
setattr(phone, 'on_return', on_return)
setattr(phone, 'on_call', on_call)
setattr(phone, 'on_undo', on_undo)
