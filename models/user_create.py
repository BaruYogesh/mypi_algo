from .fields import UserFields
from pydantic import BaseModel

class UserCreate(BaseModel):

    username: str = UserFields.username