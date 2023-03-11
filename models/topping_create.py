from .fields import ToppingFields
from pydantic import BaseModel

class ToppingCreate(BaseModel):

    topping_name: str = ToppingFields.topping_name