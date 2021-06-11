# SETPH XXXXXXXXXX
from phase_pattern import *

fyr = Phase()


def on_return(menu=None, user=None, message=None):
    # Что должна делать функция на действия, совершенные после on_call
    # Что делать с нажатой кнопкой/введёнными даннывми и т.п.
    pass


def on_call(menu=None, user=None, message=None):
	# ЧТо делает функция при вызове данной фазы
    pass


def check_access(menu, user, message):
    # Триггеры фазы
    pass


def on_undo(menu, user, message):
	# При использовании backbutton
    pass


setattr(fyr, 'check_access', check_access)
setattr(fyr, 'on_return', on_return)
setattr(fyr, 'on_call', on_call)
setattr(fyr, 'on_undo', on_undo)
