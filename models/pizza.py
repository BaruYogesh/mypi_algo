from .fields import PizzaFields
from .topping import Topping
from pydantic import BaseModel

class Pizza(BaseModel):

    toppings: list[Topping] = PizzaFields.toppings
    users: list[str] = PizzaFields.users

ListPizza = list[Pizza]