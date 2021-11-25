from state_model import PizzaOrderModel
import pytest


model = PizzaOrderModel()


@pytest.mark.parametrize('trigger', ['/start', 'Большую', 'Наличкой', 'Да'])
def test_change_state(trigger):
    model.change_state(trigger)
    model.state
