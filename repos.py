from models.room_create import RoomCreate
from models.room_update import RoomUpdate
from models.room import Room
from models.pizza import Pizza
from models.user_create import UserCreate
from models.user import User, ListUser
from models.topping_create import ToppingCreate
from models.topping import Topping, ListTopping
from db import client, collection
from utils import *
from utils import get_code
from mypi import make_pizzas_two

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
    def get_code(room_code: str) -> Room:

        doc = collection['rooms'].find_one({"room_code": room_code})

        return Room(**doc)

    @staticmethod
    def update(room_id: str, update: RoomUpdate) -> Room:

        prev_room = RoomRepo.get(room_id).dict()

        doc = update.dict()

        doc['members'] = list(set(doc['members']).union(set(prev_room['members'])))

        result = collection['rooms'].update_one({'_id': room_id}, {'$set': doc})

        return RoomRepo.get(room_id)

    @staticmethod
    def make_order(room_id: str) -> Room:

        all_toppings = [t.topping_id for t in ToppingRepo.list()]

        order = RoomRepo.get(room_id)
        users = UserRepo.list(order.members)

        prefs = {x.username: x.toppings for x in users}

        pizza_order = make_pizzas_two(all_toppings, prefs)
        pizzas: list[Pizza] = []
        for toppings, users in pizza_order:
            topping_list = [ToppingRepo.get(topping_id=t).dict() for t in toppings]
            new_pizza = Pizza(toppings=topping_list, users=users)
            print(new_pizza)
            pizzas.append(new_pizza.dict())

        print(pizzas)

        order.pizza_order = pizzas
        result = collection['rooms'].update_one({'_id': room_id}, {'$set': order.dict()})
        return RoomRepo.get(room_id)
        

class UserRepo:

    @staticmethod
    def create(create: UserCreate) -> User:

        doc = create.dict()

        doc['_id'] = get_uuid()
        doc['toppings'] = create.toppings

        result = collection['users'].insert_one(doc)

        assert result.acknowledged

        return UserRepo.get(result.inserted_id)


    @staticmethod
    def get(user_id: str) -> User:

        doc = collection['users'].find_one({"_id": user_id})

        return User(**doc)

    @staticmethod
    def list(user_ids: list[str]) -> ListUser:
        if not user_ids:
            cursor = collection['users'].find()
        else:
            cursor = collection['users'].find({"_id": {"$in": user_ids}})

        return [User(**d) for d in cursor]

class ToppingRepo:

    @staticmethod
    def create(create: ToppingCreate) -> Topping:

        doc = create.dict()

        doc['_id'] = get_uuid()

        result = collection['toppings'].insert_one(doc)

        assert result.acknowledged
        print(result.inserted_id)
        return ToppingRepo.get(result.inserted_id)

    def get(topping_id: str) -> Topping:

        doc = collection['toppings'].find_one({'_id': topping_id})

        return Topping(**doc)

    def list() -> ListTopping:
        cursor = collection['toppings'].find()

        return [Topping(**d) for d in cursor]