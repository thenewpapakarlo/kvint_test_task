from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import TOKEN


class TeleBot(object):

    def __init__(self, parent):

        self.parent = parent
        self.bot = Bot(TOKEN)
        self.dp = Dispatcher(self.bot)
        self.executor = executor

        @self.dp.message_handler(commands=['start'])
        async def welcome(message):
            await answer(message)

        @self.dp.callback_query_handler(lambda call: True)
        async def callback_inline_size(call):
            await self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
            await answer(call)

        async def answer(message):
            if isinstance(message, CallbackQuery):
                chat_id = message.message.chat.id
                trigger = message.data
            else:
                chat_id = message.chat.id
                trigger = message.text

            state_machine = self.parent.get_model('telegram', chat_id)
            if state_machine is None:
                state_machine = self.parent.add_model('telegram', chat_id)

            state_machine.change_state(trigger)
            state = state_machine.state
            keyboard = get_keyboard(state)
            message_text = state_machine.get_message(state)
            await self.bot.send_message(chat_id, message_text, reply_markup=keyboard)

        def get_keyboard(keyboard_type):
            keyboard = InlineKeyboardMarkup(row_width=2)
            if keyboard_type == 'waiting_size':
                button1 = InlineKeyboardButton('Большую', callback_data='Большую')
                button2 = InlineKeyboardButton('Маленькую', callback_data='Маленькую')
                keyboard.add(button1, button2)
            elif keyboard_type == 'waiting_payment':
                button1 = InlineKeyboardButton('Наличкой', callback_data='Наличкой')
                button2 = InlineKeyboardButton('Картой', callback_data='Картой')
                keyboard.add(button1, button2)
            elif keyboard_type == 'waiting_confirm':
                button1 = InlineKeyboardButton('Да', callback_data='Да')
                button2 = InlineKeyboardButton('Нет', callback_data='Нет')
                keyboard.add(button1, button2)
            return keyboard

        # executor.start_polling(self.dp, skip_updates=True)
