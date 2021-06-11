from phase_pattern import *
import re
from copy import deepcopy
select_pack_size = Phase()


def on_return(menu=None, user=None, message=None):
    if message.type == 'message':
        key = user.basket[-1]['key']
        if 'prod' in key:
            av_chars = list(map(str,[0,1,2,3,4,5,6,7,8,9,',','.']))
            amount = ''.join([c for c in message.content if c in av_chars]).replace(',','.')
            amount = float(amount)
            if len(re.findall('(кило|кг)',message.content)) > 0:
                weight = round(amount,1)
            elif 'гр' in message.content:
                weight = round(amount/1000,2)
            else:
                weight = round(amount,1)
        else:
            av_chars = list(map(str,[0,1,2,3,4,5,6,7,8,9,',','.']))
            amount = ''.join([c for c in message.content if c in av_chars]).replace(',','.')
            amount = int(float(amount))
            weight = amount

    else:
        weight = int(message.content)/1000

    user.basket[-1]['amount'] = weight
    product_key = user.basket[-1]['key']
    total_amount = sum([prod['amount'] for prod in user.basket if prod['key'] == product_key])
    if 'pack' in product_key:
        pack_size = user.basket[-1]['pack_size']
        total_amount *= pack_size

    if (menu.products[product_key]['in_stock'] < total_amount) and (user.id != 295932236):
        need = total_amount - menu.products[product_key]['in_stock']
        product_name = user.basket[-1]['title']
        for admin in menu.admin_list:
            menu.bot.send_message(admin, f'Недостаточно {product_name} для {user.id} (не хватает {need}кг)')

        MSG = 'На данный момент остатки продукта ограничены. При необходимости менеджер свяжется с вами для уточнения заказа.'

        menu.bot.send_message(user.id,MSG)

    key = user.basket[-1]['key']

    if 'prod' in key:
        price = deepcopy(menu.products[key]['price'])
        user.basket[-1]['price'] = int(user.basket[-1]['amount']/user.basket[-1]['pack_size']*price)
    else:
        price = deepcopy(menu.products[key]['price'])
        user.basket[-1]['price'] = int(user.basket[-1]['amount']*price)
    return user, 'NEXT', None


def on_call(menu=None, user=None, message=None):
    menu.database.to_log(user, message,'amount')
    user_id = message.user_id
    keys = menu.products.keys()
    product_key = menu.current_users[user_id].basket[-1]['key']
    # product_key = user.basket[-1].keys()
    amounts = menu.products[product_key]['amounts']

    product_name = menu.products[product_key]['description']
    product_price = menu.products[product_key]['price_desk']
    callbacks = [int(elem * 1000) for elem in amounts]

    enders = {
        'prod': ' кг.',
        'mask': ' упак.',
        'pack': ' шт.',
        'fish': ' шт.',
        'imper': ' шт.'
    }

    for elem in enders:
        if elem in product_key:
            values = [str(el) + enders[elem] for el in amounts]
            markup = select_pack_size.get_buttons(values, callbacks, cols=2, hw=False)
            break

    MSG = f'Вы выбрали {product_name} {product_price}. В каких объемах?:'
    menu.bot.send_message(user_id, MSG, reply_markup=markup)


def check_access(menu, user, message):
    if message.type == 'callback':
        pattern = '[0-9]{1,}'
        if len(re.findall(pattern,message.content)) > 0:
            return True
    elif message.type == 'message':
        pattern = '[0-9]{1,}[,.]{0,}[0-9]*.*[кгршт]{0,2}'
        if len(re.findall(pattern, message.content)) > 0:
            return True
    return False


def on_undo(menu=None,user=None,message=None):
    key = user.basket[-1]['key']
    user.basket[-1]['amount'] = None
    user.basket[-1]['price'] = menu.products[key]['price']
    return user

setattr(select_pack_size, 'on_return', on_return)
setattr(select_pack_size, 'on_call', on_call)
setattr(select_pack_size, 'check_access', check_access)
setattr(select_pack_size, 'on_undo', on_undo)
