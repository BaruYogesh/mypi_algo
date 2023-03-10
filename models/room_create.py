from .fields import RoomFields
from pydantic import BaseModel

class RoomCreate(BaseModel):

    room_name: str = RoomFields.room_name
    room_owner: str = RoomFields.room_owner