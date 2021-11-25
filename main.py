from state_model import PizzaOrderModel
from tele_bot import TeleBot
import asyncio


class MainClass(object):
    state_bots = {
        'telegram': {},
        'whatsapp': {},
    }

    def add_model(self, messenger, client_id):
        self.state_bots[messenger][client_id] = PizzaOrderModel()
        return self.state_bots[messenger][client_id]

    def get_model(self, messenger, client_id):
        return self.state_bots[messenger].get(client_id)

    def remove_model(self, messenger, client_id):
        if self.get_model(messenger, client_id):
            bots = self.state_bots[messenger]
            del bots[client_id]


def main():
    main_class = MainClass()
    tg_bot = TeleBot(main_class)
    loop = asyncio.get_event_loop()
    loop.create_task(tg_bot.executor.start_polling(tg_bot.dp, skip_updates=True))
    loop.run_forever()


if __name__ == '__main__':
    main()
