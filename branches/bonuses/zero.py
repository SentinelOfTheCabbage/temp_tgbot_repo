from phase_pattern import *

zero_func = Phase()


def on_return(menu=None, user=None, message=None):
    user.phase += 1
    return user, 'NEXT'


def on_call(menu, user=None, **data):
    menu.bot


def check_access(*args):
    return True


setattr(zero_func, 'on_return', on_return)
setattr(zero_func, 'check_access', check_access)
setattr(zero_func, 'on_call', on_call)

# del on_return, on_call, check_access
