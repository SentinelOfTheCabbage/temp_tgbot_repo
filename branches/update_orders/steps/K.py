from phase_pattern import *

name = Phase()


def on_return(menu=None, user=None, message=None):
    # Что должна делать функция на действия, совершенные после on_call
    # Что делать с нажатой кнопкой/введёнными даннывми и т.п.
    if message.type == 'callback':
        user.name = user.approx_data
    else:
        user.name = message.content
    return user, 'NEXT', None


def on_call(menu=None, user=None, message=None):
    menu.database.to_log(user, message,'name')
    user_name = menu.database.get_user_last_name(user.id)
    markup = None
    if user_name:
        user_name = user_name[0][1]
        user.approx_data = user_name
        MSG = 'Выберите или введите вручную ваше имя'
        markup = name.get_buttons([user_name],['confirm_name'], bb=False,rb=False)
    else:
        MSG = 'Как вас зовут?'
    menu.bot.send_message(user.id, MSG, reply_markup = markup)


def check_access(menu, user, message):
    # Триггеры фазы
    if message.type == 'message':
        return True
    elif message.content == 'confirm_name':
        return True
    else:
        return False


def on_undo(menu, user, message):
    # При использовании backbutton
    user.name = None
    return user

setattr(name, 'check_access', check_access)
setattr(name, 'on_return', on_return)
setattr(name, 'on_call', on_call)
setattr(name, 'on_undo', on_undo)
