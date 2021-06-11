from phase_pattern import *

promocoder = Phase()


def on_return(menu=None, user=None, message=None):
    if message.type == 'message':
        promocode = message.content
        is_available, discount, cashback = menu.database.is_code_works(
            promocode, user.id)
        if is_available and (discount + cashback > 0):
            total_price = sum([i['price'] for i in user.basket])
            if (discount > 0) and total_price * discount < 2000:
                setattr(user, 'discount', discount)
                return user, 'NEXT', None
            else:
                user.promocode = message.content
                setattr(user, 'discount', discount)
                setattr(user, 'cashback', cashback)
                result_price = sum([i['price'] for i in user.basket])

                tilda = ''
                if 'fish_forel' in set([elem['key'] for elem in user.basket]):
                    tilda = '~'
                MSG = f'Применён промокод "Первый заказ со скидкой {int(100*(1-user.discount))}%". Общая сумма заказа со скидкой {tilda}{round(result_price*user.discount)}руб.'
                menu.bot.send_message(user.id, MSG)

                return user, 'EMERGE', 1
        else:
            MSG = 'Промокод недействителен'
            menu.bot.send_message(user.id, MSG)

    return user, 'EMERGE', 0


def on_call(menu=None, user=None, message=None):
    menu.database.to_log(user, message, 'input_promocode')
    MSG = 'Введите промокод:'
    values = ['Пропустить']
    callbacks = ['miss']

    markup = promocoder.get_buttons(values, callbacks, bb=False, rb=False)

    menu.bot.send_message(user.id, MSG, reply_markup=markup)


def check_access(menu, user, message):
    if message.type == 'message':
        return True
    elif (message.content == 'miss') and (message.type == 'callback'):
        return True
    else:
        return False


def on_undo(menu, user, message):
    pass


setattr(promocoder, 'check_access', check_access)
setattr(promocoder, 'on_return', on_return)
setattr(promocoder, 'on_call', on_call)
setattr(promocoder, 'on_undo', on_undo)
