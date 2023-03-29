from .fields import PizzaFields
from .topping import Topping
from pydantic import BaseModel

class Pizza(BaseModel):

    toppings: list[Topping] = PizzaFields.toppings
    quantity: int = PizzaFields.quantity

ListPizza = list[Pizza]