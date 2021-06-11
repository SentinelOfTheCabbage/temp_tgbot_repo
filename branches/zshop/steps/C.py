from phase_pattern import *

third = Phase()


def on_return(menu=None, user=None, message=None):
    return user, 'NEXT', None


def on_call(menu=None, user=None, message=None) -> None:
    menu.database.to_log(user, message,'subresult')
    basket = user.basket
    prod_key = basket[-1]['key']
    description = menu.products[prod_key]['description']

    amount = basket[-1]['amount']
    price = basket[-1]['price']
    MSG = f'Вы выбрали "{description}", '

    if 'pack' in prod_key:
        MSG += f'{int(amount)}шт. , общая соимость {price}р'
    elif 'prod' in prod_key:
        MSG += f'вес {amount}кг. , общая стоимость {price}р '
    elif 'fish' in prod_key:
        MSG += f'{int(amount)}шт. , приблизительная стоимость {price}р'
    elif 'oyster' in prod_key:
        MSG += f'{int(amount)}шт. , общая стоимость {price}р'

    markup = third.get_buttons([], [], bb=True, gj=True)

    menu.bot.send_message(user.id, MSG, reply_markup=markup)


def check_access(menu, user, message):
    if message.content == 'gj':
        return True
    return False


def on_undo(menu=None,user=None,message=None):
    return user


setattr(third, 'on_return', on_return)
setattr(third, 'on_call', on_call)
setattr(third, 'check_access', check_access)
setattr(third, 'on_undo', on_undo)
