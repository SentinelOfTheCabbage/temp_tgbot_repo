from phase_pattern import *

phy = Phase()


def on_return(menu=None, user=None, message=None):
    # Что должна делать функция на действия, совершенные после on_call
    # Что делать с нажатой кнопкой/введёнными даннывми и т.п.
    return user, 'NEXT', None


def on_call(menu=None, user=None, message=None):
    menu.database.to_log(user, message,'result')
    # ЧТо делает функция при вызове данной фазы
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

    data = []
    #  Реорганизация Баскета юзеров для очистки дублирования наименований в ПОСЛЕДУЮЩИХ этапах (к примеру на выходе)
    for key in basket_keys:
        name = basket_names[key]
        amount = basket_amounts[key]
        price = basket_prices[key]
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
    markup = phy.get_buttons(values, callbacks, bb=False)

    result_price = sum(basket_prices.values())
    tilda = ''
    if 'fish_forel' in basket_keys:
        tilda = '~'
    MSG = f'Итого: {tilda}{result_price}руб.'

    menu.bot.send_message(user_id, MSG, reply_markup=markup)

# -------------------------------------------


def check_access(menu, user, message):
    if message.content == 'delivery_date':
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
