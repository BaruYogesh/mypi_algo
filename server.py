from fastapi import FastAPI, WebSocket, Request
from repos import *
from models import *

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post(
    "/order", 
    response_model= Room
)
async def order_post(create: RoomCreate) -> Room:
    return RoomRepo.create(create)

@app.get(
    "/order/{order_id}",
    response_model=Room
)
async def order_read(order_id: str) -> Room:
    return RoomRepo.get(order_id)

@app.patch(
    "/order/add_member/{order_id}"
)
async def order_add_member(order_id: str, update: RoomUpdate) -> Room:
    return RoomRepo.update(order_id, update)

@app.get(
    "/order/code/{room_code}",
    response_model=Room
)
async def order_read_code(room_code: str) -> Room:
    return RoomRepo.get_code(room_code)

@app.post(
    "/user",
    response_model=User
)
async def user_post(create: UserCreate) -> User:
    return UserRepo.create(create)

@app.get(
    '/user/{user_id}',
    response_model=User
)
async def user_read(user_id: str) -> User:
    return UserRepo.get(user_id)

@app.get(
    '/users'
)
async def users_read(user_ids: list[str]) -> ListUser:
    return UserRepo.list(user_ids)

@app.get(
    '/toppings/'
)
async def toppings_list() -> ListTopping:
    return ToppingRepo.list()

@app.post(
    '/topping'
)
async def topping_post(create: ToppingCreate) -> Topping:
    return ToppingRepo.create(create)