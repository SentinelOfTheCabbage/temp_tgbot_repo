from phase_pattern import *
from datetime import datetime, timedelta
import re
dox = Phase()


def on_return(menu=None, user=None, message=None):
    # Что должна делать функция на действия, совершенные после on_call
    # Что делать с нажатой кнопкой/введёнными даннывми и т.п.
    user.delivery_date = message.content
    return user, 'NEXT', None


def on_call(menu=None, user=None, message=None):
    # ЧТо делает функция при вызове данной фазы
    menu.database.to_log(user, message, 'calendar')
    if datetime.now().hour >= 12:
        DAY_DELTA = 1
    else:
        DAY_DELTA = 0
    keys = [elem['key'] for elem in user.basket]
    closest_date = None
    if 'fish_forel' in keys:
        closest_date = '11.02.21'

    if 'imper_oyster' in keys:
        PPP = True
    else:
        PPP = False

    # closest_date = None
    if closest_date != None:
        prev_val = DAY_DELTA
        DAY_DELTA = int((datetime.strptime(closest_date, '%d.%m.%y') - (datetime.now() + timedelta(hours=3))).total_seconds() / 3600 / 24 + 1)

    if DAY_DELTA < 0 :
        DAY_DELTA = prev_val

    def get_calendar(DAY_DELTA):
        markup = types.InlineKeyboardMarkup()

        months = [
            'Январь', 'Февраль', 'Март', 'Апрель',
            'Май', 'Июнь', 'Июль', 'Август',
            'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
        ]

        week_days = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
        curr_month = months[datetime.today().month - 1]
        markup.add(types.InlineKeyboardButton(text=curr_month,
                                              callback_data='Nan'))
        curr_week_day = int(
            (datetime.now() + timedelta(days=DAY_DELTA)).strftime('%w'))
        week = week_days[curr_week_day:] + week_days[:curr_week_day]

        buttons = []
        for day in week:
            buttons.append(types.InlineKeyboardButton(text=day,
                                                      callback_data='Nan'))
        for i in range(2):
            for pos, _ in enumerate(week):
                k = pos + DAY_DELTA
                cur_day = (timedelta(days=k + 7 * i) +
                           datetime.now()).strftime('%d')
                cur_mon = (timedelta(days=k + 7 * i) +
                           datetime.now()).strftime('%m')
                cont_dat = '{}.{}'.format(cur_day, cur_mon)

                cur_year = (timedelta(days=k + 7 * i) +
                            datetime.now()).strftime('%y')

                cur_date = '{}.{}.{}'.format(cur_day, cur_mon, cur_year)
                if PPP:
                    if cont_dat == '10.07':
                        buttons.append(types.InlineKeyboardButton(text=cont_dat,
                                                                  callback_data=cur_date))
                    else:
                        buttons.append(types.InlineKeyboardButton(text=' ',
                                                                  callback_data='Nan'))
                else:
                    buttons.append(types.InlineKeyboardButton(text=cont_dat,
                                                              callback_data=cur_date))

        res = []

        for i in range(7):
            res.append(buttons[i])
            res.append(buttons[i + 7])
            res.append(buttons[i + 14])
            markup.add(*res)
            res = []

        # button = types.InlineKeyboardButton(
        #     text='Ручной ввод даты', callback_data='hwd')

        # markup.add(button)

        button = types.InlineKeyboardButton(
            text='Начать заново', callback_data='restart')

        markup.add(button)

        return markup
    menu.bot.send_message(user.id, 'Выберите день доставки',
                          reply_markup=get_calendar(DAY_DELTA))


def check_access(menu, user, message):
    # Триггеры фазы
    if message.type == 'callback':
        if datetime.now().hour >= 12:
            DAY_DELTA = 1
        else:
            DAY_DELTA = 0
        current_delta = timedelta(hours=datetime.now().hour + 1)
        try:
            if datetime.strptime(message.content, '%d.%m.%y') + current_delta >= (datetime.now() + timedelta(DAY_DELTA)) and (message.type == 'callback'):
                return True
            else:
                return False
        except Exception as e:
            return False
    else:
        if not re.fullmatch('[0-9]{2}\.[0-9]{2}', message.content):
            return False

        input_info = message.content
        message.content = input_info + f'.{datetime.now().strftime("%y")}'
        date = datetime.strptime(message.content,'%d.%m.%y')

        if timedelta(days=13) < date - datetime.now() < timedelta(days=31):
            return True
        else:
            message.content = input_info + f'.{int(datetime.now().strftime("%y"))+1}'
            date = datetime.strptime(message.content,'%d.%m.%y')
            if date - datetime.now() < timedelta(days=31):
                return True
            else:
                message.content = ''
                return False

def on_undo(menu, user, message):
    # При использовании backbutton
    user.delivery_date = None
    return user

setattr(dox, 'check_access', check_access)
setattr(dox, 'on_return', on_return)
setattr(dox, 'on_call', on_call)
setattr(dox, 'on_undo', on_undo)
