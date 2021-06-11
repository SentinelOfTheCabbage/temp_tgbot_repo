from phase_pattern import *

phy = Phase()


def on_return(menu=None, user=None, message=None):
    if (message.content == 'promocode') and (message.type == 'callback'):
        return user, 'DIVE', ['promocode',0]
    else:
        return user, 'NEXT', None


def on_call(menu=None, user=None, message=None):
    menu.database.to_log(user, message,'result')
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
            user.basket[j]['amount'] += user.basket[i]['amount']
            user.basket[j]['price'] += user.basket[i]['price']
        else:
            cp_keys[user.basket[i]['key']] = i
    user.basket = [user.basket[i] for i in cp_keys.values()]

    # print(user.basket)

    data = []
    #  Реорганизация Баскета юзеров для очистки дублирования наименований в ПОСЛЕДУЮЩИХ этапах (к примеру на выходе)
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
        values.append('{} [х{}] - {}  руб'.format(n,
                                                  round(a, 2), round(p)))
        callbacks.append('Nan')

    values.append('Корректировать заказ')
    values.append('Выбрать дату доставки')

    callbacks.append('restart')
    callbacks.append('delivery_date')
    if not user.promocode:
        values.append('Ввести промокод')
        callbacks.append('promocode')

    markup = phy.get_buttons(values, callbacks, bb=False)

    result_price = sum(basket_prices.values())
    tilda = ''
    if 'fish_forel' in basket_keys:
        tilda = '~'
    if user.promocode:
        MSG = f'Применён промокод "Первый заказ со скидкой {int(100*(1-user.discount))}%". Общая сумма заказа со скидкой {tilda}{round(result_price*user.discount)}руб.'
    else:
        MSG = f'Итого: {tilda}{result_price}руб.'

    bonuses = menu.database.get_bonuses(user_id)
    if bonuses and (bonuses[0][0] > 0):
        bonuses = bonuses[0][0]
        if user.promocode:
            t = round(result_price*user.discount)
        else:
            t = result_price

        if bonuses <= t:
            user.bonuses = bonuses
        else:
            user.bonuses = t

        MSG += f', из них {user.bonuses} руб. оплачивается за счёт накопленных бонусов'

    menu.bot.send_message(user_id, MSG, reply_markup=markup)

# -------------------------------------------


def check_access(menu, user, message):
    # Триггеры фазы
    if message.content in ['delivery_date','promocode']:
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
