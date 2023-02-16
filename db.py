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

class Group(BaseModel):
    group_id = AutoField()
    group_code = CharField()
    active = BooleanField()
    group_name = CharField()
    group_owner = ForeignKeyField(User)

db.connect()
db.create_tables([User, Topping])