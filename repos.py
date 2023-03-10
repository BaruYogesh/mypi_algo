from models.room_create import RoomCreate
from models.room_update import RoomUpdate
from models.room import Room
from models.user_create import UserCreate
from models.user import User
from db import client, collection
from utils import *
from utils import get_code

class RoomRepo:

    @staticmethod
    def create(create: RoomCreate) -> Room:

        doc = create.dict()

        doc['_id'] = get_uuid()

        new_code = get_code()
        while collection['rooms'].find_one({'room_code': new_code}) is not None:
            new_code = get_code()
        doc['room_code'] = new_code

        doc['members'] = []
        doc['pizza_order'] = []

        result = collection['rooms'].insert_one(doc)

        assert result.acknowledged

        return RoomRepo.get(result.inserted_id)

    @staticmethod
    def get(room_id: str) -> Room:

        doc = collection['rooms'].find_one({"_id": room_id})

        return Room(**doc)

    @staticmethod
    def update(room_id: str, update: RoomUpdate):
        doc = update.dict()

        result = collection['rooms'].update_one({'_id': room_id}, {'$set': doc})

class UserRepo:

    @staticmethod
    def create(create: UserCreate) -> User:

        doc = create.dict()

        doc['_id'] = get_uuid()
        doc['toppings'] = []

        result = collection['users'].insert_one(doc)

        assert result.acknowledged

        return UserRepo.get(result.inserted_id)


    @staticmethod
    def get(user_id: str) -> User:

        doc = collection['users'].find_one({"_id": user_id})

        return User(**doc)