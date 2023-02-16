from flask import Flask, request
import random
import db

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# @app.route('/room', methods=['GET', 'POST', 'DELETE'])
# def create_room():
#     if request.method == 'POST'