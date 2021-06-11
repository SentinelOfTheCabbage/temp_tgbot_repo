from phase_pattern import *
from datetime import datetime
import re
time = Phase()


def on_return(menu=None, user=None, message=None):
    user.delivery_time = message.content
    return user, 'NEXT', None


def on_call(menu=None, user=None, message=None):
    menu.database.to_log(user, message,'time')
    result_price = sum([e['price'] for e in user.basket])

    if user.delivery_date == datetime.now().strftime('%d.%m.%y'):
        if 10 <= datetime.now().hour < 12:
            values = [' ','17-20', '20-23']
            callbacks = [e.replace('-', 'to') for e in values]
        if datetime.now().hour < 10:
            values = ['14-17', '17-20', '20-23']
            callbacks = [e.replace('-', 'to') for e in values]
    else:
        values = ['11-14', '14-17', '17-20', '20-23']
        callbacks = [e.replace('-', 'to') for e in values]

    markup = time.get_buttons(values, callbacks, cols=3,appender=False)

    menu.bot.send_message(user.id, 'В какой временной промежуток?',
                          reply_markup=markup)


def check_access(menu, user, message):
    # Триггеры фазы
    pattern = '[0-9]{1,2}to[0-9]{1,2}'
    if message.type == 'callback' and len(re.findall(pattern, message.content)):
        return True
    else:
        return False


def on_undo(menu, user, message):
    # При использовании backbutton
    user.delivery_time = message.content
    return user

setattr(time, 'check_access', check_access)
setattr(time, 'on_return', on_return)
setattr(time, 'on_call', on_call)
setattr(time, 'on_undo', on_undo)
