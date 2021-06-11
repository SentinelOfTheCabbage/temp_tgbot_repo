from phase_pattern import *
from copy import deepcopy
from datetime import datetime

second = Phase()


def on_return(menu=None, user=None, message=None):
    return user, 'CURRENT', 0


def on_call(menu=None, user=None, message=None):
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
        total_order.append(f'Курьер прибудет {datetime.now().strftime("%d.%m.%y")} c {courier_time}:30 - {courier_time+1}:00')
        total_order.append('---------------------')

    if len(total_order) > 0:
        MSG = 'На текущий момент необходимо:\n\n' + '\n'.join(total_order)
    else:
        MSG = 'На текущий момент ничего не нужно'

    if len(MSG) > 4096:
        parts = [MSG[4096 * i: 4096 * (i + 1)]
                 for i in range(100) if 4096 * (i + 1) < len(MSG)]
        parts.append(MSG[-(len(MSG) % 5):])
        for msg_part in parts:
            menu.bot.send_message(user.id, msg_part)
    else:
        menu.bot.send_message(user.id, MSG)


def check_access(menu, user, message):
    return False


def on_undo(menu=None, user=None, message=None):
    return user


setattr(second, 'on_call', on_call)
setattr(second, 'check_access', check_access)
setattr(second, 'on_return', on_return)
setattr(second, 'on_undo', on_undo)