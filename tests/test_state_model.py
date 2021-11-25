from state_model import PizzaOrderModel
import pytest


model = PizzaOrderModel()
messages = [
    'Какую вы хотите пиццу? Большую или маленькую?',
    'Как вы будете платить?',
    'Вы хотите {} пиццу, оплата - {}?',
    'Спасибо за заказ'
]
i = 0


@pytest.mark.parametrize('trigger', ['/start', 'Большую', 'Наличкой', 'Да'])
def test_change_state(trigger):
    model.change_state(trigger)
    global i
    assert messages[i] == model.questions[model.state]
    i += 1
