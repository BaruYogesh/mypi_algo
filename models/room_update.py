from pydantic import BaseModel
from typing import Optional, List
from .fields import RoomFields
from .user import User

class RoomUpdate(BaseModel):
    room_name: Optional[str] = RoomFields.room_name
    members: Optional[List[str]] = RoomFields.members

    def dict(self, **kwargs):
        d = super().dict(**kwargs)
        res = {k:v for k,v in d.items() if v is not None}
        print(res)
        return res