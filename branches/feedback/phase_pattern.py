from telebot import types

class Phase:

    def __init__(check_function=None, *data):
        pass

    def on_return(self, menu, user=None, message=None):
        # Что должна делать функция на действия, совершенные после on_call
        # Что делать с нажатой кнопкой/введёнными даннывми и т.п.
        print('on_return')
        return user

    def on_call(self, menu, user, message):
        # ЧТо делает функция при вызове данной фазы
        print('on_call')
        pass

    def check_access(self, user, message):
        # Триггеры фазы
        print('check_access')
        pass

    def on_undo(self, menu,user,message):
        # При использовании backbutton
        pass

    def get_next(self, user, message):
        # ХЗ пока =/
        return 'NEXT'

    def get_buttons(self, values, keys, step=0, cols=1, bb=True, hw=False, gj=False, fb=False, rb=True, refb=False, appender=False):
        buttons = []
        markup = types.InlineKeyboardMarkup()
        if appender is True:
            if len(values) % cols != 0:
                k = cols - (len(values) % cols)
                for i in range(k):
                    values.append(' ')
                    keys.append('Nan')

        for pos, data in enumerate(list(zip(values, keys))):
            text = data[0]
            callback = data[1]
            buttons.append(types.InlineKeyboardButton(
                text=text, callback_data=callback))
            if (pos + 1) % cols == 0:
                markup.add(*buttons)
                buttons = []

        if bb is True:
            buttons.append(types.InlineKeyboardButton(
                text='Назад', callback_data='back'))
        if hw is True:
            buttons.append(types.InlineKeyboardButton(
                text='Ручной ввод', callback_data='hw'))
        if gj is True:
            buttons.append(types.InlineKeyboardButton(
                text='Всё верно', callback_data='gj'))
        if fb is True:
            fb_url = 'https://docs.google.com/forms/d/e/1FAIpQLSfMtq2osoMw0b7iytBjaEyw4yBhimHzan3JlqGZfYK3rrhwfw/viewform?usp=sf_link'

            buttons.append(types.InlineKeyboardButton(
                text='Обратная связь', url=fb_url))
        if refb is True:
            buttons.append(types.InlineKeyboardButton(
                text='Получить ссылку', callback_data='referr'))
        if rb is True:
            buttons.append(types.InlineKeyboardButton(
                text='Начать заново', callback_data='restart'))
        while len(buttons) // cols > 0:
            markup.add(*buttons[:cols])
            buttons = buttons[cols:]

        markup.add(*buttons)
        return markup
