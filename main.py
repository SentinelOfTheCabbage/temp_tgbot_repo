#pylint: disable=C0111, W0401,W0614
from telebot        import TeleBot, types
from main_menu      import *
from branches       import *
from settings       import *
from time           import sleep
import traceback
BOT = TeleBot(TOKEN)
MAIN_MENU = main_menu(BOT)

# @BOT.callback_query_handler(func=lambda call: call.data == 'referr')
def referr(call) -> None:
    chat_id = call.message.chat.id
    markup = types.InlineKeyboardMarkup()
    ref_btn = types.InlineKeyboardButton(
        'Нажми и удерживай!',
        url=f'tg://resolve?domain={DOMAIN}&start={chat_id}'
    )
    markup.add(ref_btn)
    restart_button = types.InlineKeyboardButton(
        text='Начать заново', callback_data='restart')
    markup.add(restart_button)

    msg = 'Ваша личная ссылка - это возможность получить 400 фиш-бонусов за каждого нового' + \
        'клиента, сделавшего заказ через вашу личную ссылку. 1 фиш-бонус = 1 рубль скидки' + \
        ' в нашем магазине морепродуктов. Копируй ссылку и делись ею.'
    BOT.send_message(chat_id, msg, reply_markup=markup)

@BOT.message_handler(commands=['give_menu'])
def aX(message):
    user_id = message.from_user.id
    BOT.send_document(
        user_id,
        MENU_FILE_TOKEN
    )

@BOT.callback_query_handler(func=lambda message: True if 'give_menu' == message.data else False)
def aX(message):
    user_id = message.from_user.id
    BOT.send_document(
        user_id,
        MENU_FILE_TOKEN
    )

@BOT.message_handler(commands=['feedback'])
def asdasd(message) -> None:
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup()
    ref_btn = types.InlineKeyboardButton('Нажми и удерживай!', callback_data='feedback_collector')
    markup.add(ref_btn)

    BOT.send_message(user_id, 'Hello!', reply_markup=markup)

@BOT.message_handler(func=lambda message: True)
def reaction(message) -> None:
    if message.text == '/start give_menu':
        user_id = message.from_user.id
        BOT.send_document(
            user_id,
            MENU_FILE_TOKEN
        )
        return None
    try:
        MAIN_MENU.get_reaction(message=message)
    except Exception as e:
        traceback.print_exc()
        MAIN_MENU.clear_users()
        BOT.send_message(295932236, traceback.format_exc())

@BOT.callback_query_handler(func=lambda call: call.data != 'Nan')
def clbk(call) -> None:
    # MAIN_MENU.get_reaction(callback=call)

    try:
        MAIN_MENU.get_reaction(callback=call)
    except Exception as e:
        traceback.print_exc()
        MAIN_MENU.clear_users()
        BOT.send_message(295932236, traceback.format_exc())

while True:
    print('STARTING')
    BOT.polling(none_stop=True)

