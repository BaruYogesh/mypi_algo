from peewee import *

db = SqliteDatabase('my_database.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)
    user_id = AutoField()

class Topping(BaseModel):
    topping_name = CharField(unique=True)

class Pizza_Order(BaseModel):
    room_id = ForeignKeyField(Room)

class Room(BaseModel):
    room_id = AutoField()
    room_code = CharField()
    active = BooleanField()
    room_name = CharField()
    room_owner = ForeignKeyField(User)
    pizza_order = ForeignKeyField(Pizza_Order)

class Room_Membership(BaseModel):
    user_id = ForeignKeyField(User)
    room_id = ForeignKeyField(Room)



db.connect()
db.create_tables([User, Topping])