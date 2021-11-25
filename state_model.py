from transitions import Machine


class PizzaOrderModel(object):
    states = ['waiting_size', 'waiting_payment', 'waiting_confirm', 'done']
    messages = [
        'Какую вы хотите пиццу? Большую или маленькую?',
        'Как вы будете платить?',
        'Вы хотите {} пиццу, оплата - {}?',
        'Спасибо за заказ'
    ]

    def __init__(self):
        self.size = None
        self.payment = None
        self.questions = {state: message for state, message in zip(PizzaOrderModel.states, PizzaOrderModel.messages)}
        self.machine = Machine(self, states=PizzaOrderModel.states, initial='waiting_size')
        self.machine.add_transition(trigger='Большую', source='waiting_size', dest='waiting_payment', before='big_size')
        self.machine.add_transition(trigger='Маленькую', source='waiting_size', dest='waiting_payment',
                                    before='small_size')
        self.machine.add_transition(trigger='Наличкой', source='waiting_payment', dest='waiting_confirm',
                                    before='cash_payment')
        self.machine.add_transition(trigger='Картой', source='waiting_payment', dest='waiting_confirm',
                                    before='card_payment')
        self.machine.add_transition(trigger='Да', source='waiting_confirm', dest='done', before='reset')
        self.machine.add_transition(trigger='Нет', source='waiting_confirm', dest='waiting_size', before='reset')
        self.machine.add_transition(trigger='/start', source='*', dest='waiting_size', before='reset')

    def change_state(self, trigger):
        self.machine.dispatch(trigger)

    def big_size(self):
        self.size = 'Большую'

    def small_size(self):
        self.size = 'Маленькую'

    def cash_payment(self):
        self.payment = 'Наличкой'

    def card_payment(self):
        self.payment = 'Картой'

    def reset(self):
        self.size = None
        self.payment = None

    def get_message(self, state):
        return self.questions[state].format(str(self.size).lower(), str(self.payment).lower())
