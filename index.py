from mysql import connector
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from room import Room

app = Flask(__name__)
socketio = SocketIO(app)

mydb = connector.connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    database='projeto_pp'
)

mycursor = mydb.cursor()

rooms = {}

@app.route('/')
def index():
    #query = "select id, nome from objetos where id_categoria = 1 and id_subcategoria=1"
    #mydb.cmd_query(query)

    mycursor.execute("select id, nome from categorias")
    categorias = mycursor.fetchall()
    
    mycursor.execute("select id_categoria, nome from subcategorias")
    
    subcategorias = mycursor.fetchall()

    for x in categorias:
        print(x[0])

    return render_template('index.html', categorias=categorias, subcategorias=subcategorias)

@app.route('/room/<int:room_id>')
def room(room_id):

    return render_template('room.html', room_id = room_id)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = rooms.get(int(data['room']))
    join_room(int(data['room']))

    print(username + ' has entered the room: ' + data['room'])

    #update server rooms
    if not room:
        rooms.setdefault(int(data['room']), Room(int(data['room'])))
        room = rooms.get(int(data['room']))

    room.addPlayer(request.sid)
    room.sendDraw(socketio, request.sid)

    #start game with 2 or more players
    if(not room.isPlaying()):
        if(room.getPlayersCount() > 1):
            print("game start")
        else:
            print("waiting for players")


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = int(data['room'])
    leave_room(room)

    print(username + ' has left the room: ' + str(room))

    #update server rooms

    if  rooms.get(room).removePlayer(request.sid):
        rooms.pop(room)
        

# response to remote object call
@socketio.on("request invoke")
def invoke(data):
    room = int(data['room'])
    rooms.get(room).addCommand(data)
    emit("invoke method", data, include_self=False, room = room)
