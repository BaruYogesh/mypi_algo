from .fields import UserFields
from .user_create import UserCreate
from .topping import Topping
from typing import List
import pydantic

class User(UserCreate):

    user_id: str = UserFields.user_id
    toppings: List[Topping] = UserFields.toppings_liked

    @pydantic.root_validator(pre=True)
    def _set_user_id(cls, data):
        """Swap the field _id to user_id (this could be done with field alias, by setting the field as "_id"
        and the alias as "user_id", but can be quite confusing)"""
        document_id = data.get("_id")
        if document_id:
            data["user_id"] = document_id
        return data