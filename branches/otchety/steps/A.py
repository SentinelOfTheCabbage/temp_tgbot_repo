from phase_pattern import *
from copy import deepcopy
from datetime import datetime, timedelta
import re
first = Phase()


def on_return(menu=None, user=None, message=None):
    setattr(user, 'search_date', message.content)

    needed_date = datetime.strptime(user.search_date, '%d.%m.%Y')
    current_date = datetime.strptime(datetime.now().strftime('%d.%m.%Y'), '%d.%m.%Y')
    delta = needed_date - current_date

    orders_id_list = menu.database.get_order_id_list(delta.days)
    total_order = []
    for id, dest_time, address, name, phone in orders_id_list:
        products = menu.database.get_products_by_order_id(id)
        courier_time = int(dest_time[:dest_time.find('to')]) - 1
        total_order.append(f'Заказ №{id}\n')
        total_order.append(f'{name} - {phone}\n')
        for title, key, pack_size, amount in products:
            res_count = round(amount / pack_size, 1)
            if 'prod' in key:
                suffix = 'кг'
            elif 'fish' in key:
                suffix = 'шт'
                res_count = amount
            else:
                suffix = 'шт'

            total_order.append(f'--{title}: [x{amount}] {res_count} по {round(1000*pack_size,1)} ')
        total_order.append(f'Адрес доставки: {address}')
        total_order.append(f'Курьер прибудет {needed_date.strftime("%d.%m.%y")} c {courier_time}:30 - {courier_time+1}:00')
        total_order.append('---------------------')

    if len(total_order) > 0:
        MSG = 'На текущий момент необходимо:\n\n' + '\n'.join(total_order)
    else:
        MSG = 'На текущий момент ничего не нужно'
    # print(MSG)

    if len(MSG) > 4096:
        parts = []
        i = 0
        while len(''.join(parts)) < len(MSG):
            parts.append(MSG[4096*i:4096*(i+1)])
            i += 1
        # parts = [MSG[4096 * i: 4096 * (i + 1)]
        #          for i in range(100) if 4096 * (i + 1) < len(MSG)]
        # parts.append(MSG[-(len(MSG) % 5):])
        for msg_part in parts:
            menu.bot.send_message(user.id, msg_part)
    else:
        menu.bot.send_message(user.id, MSG)

    return user, 'CURRENT', None


def on_call(menu=None, user=None, message=None):
    def get_calendar():
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
        curr_week_day = int(datetime.now().strftime('%w'))
        week = week_days[curr_week_day:] + week_days[:curr_week_day]

        buttons = []
        for day in week:
            buttons.append(types.InlineKeyboardButton(text=day,
                                                      callback_data='Nan'))
        for i in range(2):
            for pos, _ in enumerate(week):
                k = pos
                cur_day = (timedelta(days=k + 7 * i) +
                           datetime.now()).strftime('%d')
                cur_mon = (timedelta(days=k + 7 * i) +
                           datetime.now()).strftime('%m')
                cont_dat = '{}.{}'.format(cur_day, cur_mon)

                cur_year = (timedelta(days=k + 7 * i) +
                            datetime.now()).strftime('%Y')

                cur_date = '{}.{}.{}'.format(cur_day, cur_mon, cur_year)
                buttons.append(types.InlineKeyboardButton(text=cont_dat,
                                                          callback_data=cur_date))

        res = []

        for i in range(7):
            res.append(buttons[i])
            res.append(buttons[i + 7])
            res.append(buttons[i + 14])
            markup.add(*res)
            res = []
        return markup

    markup = get_calendar()
    menu.bot.send_message(user.id, 'Calendar: ', reply_markup=markup)


def check_access(menu, user, message):
    if re.findall('[0-9]{2}.[0-9]{2}.[0-9]{4}', message.content):
        return True
    else:
        return False


def on_undo(menu=None, user=None, message=None):
    return user


setattr(first, 'on_call', on_call)
setattr(first, 'check_access', check_access)
setattr(first, 'on_return', on_return)
setattr(first, 'on_undo', on_undo)
# del on_call, on_return, check_access
