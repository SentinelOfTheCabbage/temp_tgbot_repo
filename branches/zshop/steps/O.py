from phase_pattern import *

promoPhase = Phase()


def on_return(menu=None, user=None, message=None):
    # import pdb; pdb.set_trace();
    return user, message.content, 0


def on_call(menu=None, user=None, message=None):
    menu.database.to_log(user, message, 'promocode_sol')

    total_price = sum([i['price'] for i in user.basket])
    MSG = f'Для применения скидки - добавьте продукты на {round(2223 - total_price)} руб.'

    delattr(user,'discount')

    values = ['Продолжить покупки', 'Купить без скидки']
    callbacks = ['BEFORE_PROMO', 'AFTER_PROMO']

    markup = promoPhase.get_buttons(values, callbacks, bb=False, rb=True)

    menu.bot.send_message(user.id, MSG, reply_markup=markup)

def check_access(menu, user, message):
    if message.content in ['BEFORE_PROMO','AFTER_PROMO','restart']:
        return True
    else:
        return False


def on_undo(menu, user, message):
    pass


setattr(promoPhase, 'check_access', check_access)
setattr(promoPhase, 'on_return', on_return)
setattr(promoPhase, 'on_call', on_call)
setattr(promoPhase, 'on_undo', on_undo)
