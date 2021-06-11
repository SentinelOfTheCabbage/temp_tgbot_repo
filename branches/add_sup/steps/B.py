from phase_pattern import *
import re
from copy import deepcopy
select_pack_size = Phase()


def on_return(menu=None, user=None, message=None):
    product_key = user.basket[-1]['key']
    if message.type == 'message':
        av_chars = list(map(str, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ',', '.']))
        amount = ''.join(
            [c for c in message.content if c in av_chars]).replace(',', '.')
        amount = float(amount)
        if 'prod' in product_key:
            if 'гр' in message.content:
                weight = round(amount / 1000, 2)
            else:
                weight = round(amount, 1)
        else:
            amount = int(amount)
            weight = amount
    else:
        weight = int(message.content) / 1000

    if 'oyster' in product_key:
        if weight < 6:
            weight = 6

    user.basket[-1]['amount'] += weight

    total_amount = sum([prod['amount']
                        for prod in user.basket if prod['key'] == product_key])
    if 'pack' in product_key:
        pack_size = user.basket[-1]['pack_size']
        total_amount *= pack_size

    if 'prod' in product_key:
        price = deepcopy(menu.products[product_key]['price'])
        user.basket[-1]['price'] = round(user.basket[-1]
                                         ['amount'] / user.basket[-1]['pack_size'] * price)
    else:
        price = deepcopy(menu.products[product_key]['price'])
        user.basket[-1]['price'] = round(user.basket[-1]['amount'] * price)

    return user, 'NEXT', None


def on_call(menu=None, user=None, message=None):
    # menu.database.to_log(user, message,'amount')
    user_id = message.user_id
    keys = menu.products.keys()
    product_key = user.basket[-1]['key']
    amounts = menu.products[product_key]['amounts']

    product_name = user.basket[-1]['title']
    product_price = user.basket[-1]['price_desk']
    callbacks = [int(elem * 1000) for elem in amounts]

    enders = {
        'prod': ' кг.',
        'mask': ' упак.',
        'pack': ' шт.',
        'fish': ' шт.',
        'imper': ' шт.',
    }

    current_size = enders[[x for x in enders if x in product_key][0]]

    MSG = f'Вы выбрали {product_name}. Сколько {current_size}?:'
    menu.bot.send_message(user_id, MSG)


def check_access(menu, user, message):
    if message.type == 'message':
        pattern = '[0-9]{1,}[,.]{0,}[0-9]*.*[кгршт]{0,2}'
        if len(re.findall(pattern, message.content)) > 0:
            return True
    return False


def on_undo(menu=None, user=None, message=None):
    key = user.basket[-1]['key']
    user.basket[-1]['amount'] = None
    user.basket[-1]['price'] = menu.products[key]['price']
    return user

setattr(select_pack_size, 'on_return', on_return)
setattr(select_pack_size, 'on_call', on_call)
setattr(select_pack_size, 'check_access', check_access)
setattr(select_pack_size, 'on_undo', on_undo)
