from phase_pattern import Phase

third = Phase()


def on_return(menu=None, user=None, message=None) -> ():
    user.basket[-1]['price'] = int(message.content) * \
        user.basket[-1]['amount'] / user.basket[-1]['amounts'][0]
    return user, 'NEXT', None


def on_call(menu=None, user=None, message=None):
    menu.database.to_log(user, message, 'subresult')
    basket = user.basket
    prod_key = basket[-1]['key']
    description = menu.products[prod_key]['description']

    amount = basket[-1]['amount']
    price = basket[-1]['price']
    MSG = f'Вы выбрали "{description}", '

    if 'pack' in prod_key:
        MSG += f'{amount}шт.'
    elif 'prod' in prod_key:
        MSG += f'вес {amount}кг.'
    elif 'fish' in prod_key:
        MSG += f'{amount}шт.'
    MSG += '\nВведите стоимость за единицу:'

    markup = third.get_buttons([], [], bb=True)
    menu.bot.send_message(user.id, MSG, reply_markup=markup)


def check_access(menu=None, user=None, message=None) -> bool:
    if message.type == 'message' and message.content.isnumeric():
        return True
    return False


def on_undo(menu=None, user=None, message=None):
    return user


setattr(third, 'on_return', on_return)
setattr(third, 'on_call', on_call)
setattr(third, 'check_access', check_access)
setattr(third, 'on_undo', on_undo)
