from pydantic import Field

class UserFields:

    username = Field()
    user_id = Field()
    toppings_liked = Field(
        description='list of toppings the user prefers'
    )

class RoomFields:

    room_id = Field()
    room_name = Field()
    room_code = Field()
    room_owner = Field(
        description='user object of the user who owns this room'
    )
    members = Field(
        description='list of users who belong to this room'
    )
    pizza_order = Field(
        description='list of pizza objects for every pizza order'
    )

class PizzaFields:

    toppings = Field(
        description='list of topping objects'
    )
    users = Field()

class ToppingFields:

    topping_id = Field()
    topping_name = Field()
