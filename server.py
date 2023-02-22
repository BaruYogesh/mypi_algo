from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import random

app = Flask(__name__)

socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app)

@app.get('/toppings')
def toppings():
    pass # return all toppings

@app.route('/order', methods=['POST', 'PUT', 'DELETE'])
def order():
    if request.method == 'POST':
        pass # organizer creates an order
    elif request.method == 'PUT':
        pass # user joins a room
    elif request.method == 'DELETE':
        pass # organizer closes a room

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)
