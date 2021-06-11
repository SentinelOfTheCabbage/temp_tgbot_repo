from phase_pattern import *

phy = Phase()


def on_return(menu=None, user=None, message=None):
    msg = 'NEXT'
    return user, msg, None


def on_call(menu=None, user=None, message=None):
    # menu.database.to_log(user, message,'result')
    user_id = user.id
    basket = user.basket

    basket_keys = set([elem['key'] for elem in basket])
    basket_amounts = {key: 0 for key in basket_keys}
    basket_prices = {key: 0 for key in basket_keys}
    basket_names = {key: menu.products[key]['title']
                    for key in menu.products if key in basket_keys}

    for product in basket:
        key = product['key']
        basket_amounts[key] += product['amount']
        basket_prices[key] += product['price']

    cp_keys = {}
    for i in range(len(user.basket)):
        if user.basket[i]['key'] in cp_keys:
            j = cp_keys[user.basket[i]['key']]
            user.basket[j]['price'] = user.basket[j][
                'price'] / user.basket[j]['amount'] + user.basket[i]['price'] / user.basket[i]['amount']

            user.basket[j]['amount'] += user.basket[i]['amount']
        else:
            cp_keys[user.basket[i]['key']] = i

    user.basket = [user.basket[i] for i in cp_keys.values()]

    data = []
    for prod in user.basket:
        name = prod['title']
        amount = prod['amount']
        price = prod['price']
        data.append([name, amount, price])

    values = []
    callbacks = []

    for n, a, p in data:
        if len(n) > 11:
            n = n[:8] + '...'
        values.append('{} [х{}] - {}  руб/[шт./кг./упак.]'.format(n,
                                                                  round(a, 2), round(p)))
        callbacks.append('Nan')

    values.append('Корректировать поставку')
    callbacks.append('restart')

    markup = phy.get_buttons(values, callbacks, bb=False, gj=True)

    MSG = f'Итого:'
    menu.bot.send_message(user_id, MSG, reply_markup=markup)


def check_access(menu, user, message):
    if message.content == 'gj':
        return True
    else:
        return False


def on_undo(menu, user, message):
    # При использовании backbutton
    return user


setattr(phy, 'check_access', check_access)
setattr(phy, 'on_return', on_return)
setattr(phy, 'on_call', on_call)
setattr(phy, 'on_undo', on_undo)
