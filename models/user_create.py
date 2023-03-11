from .fields import UserFields
from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):

    username: str = UserFields.username
    toppings: List[str] = UserFields.toppings_liked
