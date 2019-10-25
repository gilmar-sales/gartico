from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/room/<int:room_id>')
def room(room_id):
    return render_template('room.html', room_id = room_id)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    print(username + ' has entered the room: ' + room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    print(username + ' has left the room: ' + room)

# response to remote object call
@socketio.on("request invoke")
def invoke(data):
    emit("invoke method", data, include_self=False, room = data['room'])
