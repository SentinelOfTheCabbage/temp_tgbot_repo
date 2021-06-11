from phase_pattern import *

third = Phase()


def on_return(menu=None, user=None, message=None):
    price = ''.join(
        [i for i in message.content if i in '1234567890,.']).replace(',', '.')
    price = float(price)
    user.basket[-1]['price'] = price
    return user, 'NEXT', None


def on_call(menu=None, user=None, message=None) -> None:
    # menu.database.to_log(user, message, 'subresult')
    basket = user.basket
    prod_key = basket[-1]['key']
    description = menu.products[prod_key]['description']

    amount = basket[-1]['amount']
    price = basket[-1]['price']

    enders = {
        'prod': ' кг.',
        'mask': ' упак.',
        'pack': ' шт.',
        'fish': ' шт.',
        'imper': ' шт.',
    }
    current_size = enders[[x for x in enders if x in prod_key][0]]
    MSG = f'Введите стоимость за 1 {current_size}:'

    markup = third.get_buttons([], [], bb=True)
    menu.bot.send_message(user.id, MSG, reply_markup=markup)


def check_access(menu, user, message):
    price = ''.join(
        [i for i in message.content if i in '1234567890,.']).replace(',', '.')
    if len(price) == len(message.content):
        return True
    return False


def on_undo(menu=None, user=None, message=None):
    return user


setattr(third, 'on_return', on_return)
setattr(third, 'on_call', on_call)
setattr(third, 'check_access', check_access)
setattr(third, 'on_undo', on_undo)
