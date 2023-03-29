from .fields import RoomFields
from .room_create import RoomCreate
from .pizza import Pizza
from typing import List, Optional
import pydantic

class Room(RoomCreate):

    room_id: str = RoomFields.room_id
    room_code: str = RoomFields.room_code
    members: Optional[List[str]] = RoomFields.members
    pizza_order: Optional[List[Pizza]] = RoomFields.pizza_order


    @pydantic.root_validator(pre=True)
    def _set_room_id(cls, data):
        """Swap the field _id to room_id (this could be done with field alias, by setting the field as "_id"
        and the alias as "room_id", but can be quite confusing)"""
        document_id = data.get("_id")
        if document_id:
            data["room_id"] = document_id
        return data