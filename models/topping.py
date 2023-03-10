from .fields import ToppingFields
from pydantic import BaseModel

class Topping(BaseModel):

    topping_id: str = ToppingFields.topping_id
    name: str = ToppingFields.name