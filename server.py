from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import random
import db
from models import *

app = Flask(__name__)
client = db.get_database()
socketio = SocketIO(app)

if __name__ == "__main__":
    socketio.run(app)

@app.get('/')
def hello_world():
    return 'hello world'

@app.get("/toppings")
def toppings():
    pass  # return all toppings


@app.route("/order", methods=["POST", "PUT", "DELETE"])
def order():
    print('order')
    if request.method == "POST": # organizer creates an order
        order_codes = client['rooms']

        new_code = make_code()
        while order_codes.find_one({'room_code': new_code}) is not None:
            new_code = make_code()

        new_room = order_codes.insert_one({
            'room_code': new_code
        })

        return {'room_code': new_code}

    elif request.method == "PUT":
        pass  # user joins a room
    elif request.method == "DELETE":
        pass  # organizer closes a room


@socketio.on("join")
def on_join(data):
    username = data["username"]
    room = data["room"]
    join_room(room)
    send(username + " has entered the room.", to=room)

@socketio.on("leave")
def on_leave(data):
    username = data["username"]
    room = data["room"]
    leave_room(room)
    send(username + " has left the room.", to=room)
