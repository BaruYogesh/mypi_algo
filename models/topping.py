from .fields import ToppingFields
from .topping_create import ToppingCreate
import pydantic

class Topping(ToppingCreate):

    topping_id: str = ToppingFields.topping_id

    @pydantic.root_validator(pre=True)
    def _set_topping_id(cls, data):
        """Swap the field _id to topping_id (this could be done with field alias, by setting the field as "_id"
        and the alias as "topping_id", but can be quite confusing)"""
        document_id = data.get("_id")
        if document_id:
            data["topping_id"] = document_id
        return data

ListTopping = list[Topping]