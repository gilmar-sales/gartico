from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_socketio import SocketIO, emit, join_room, leave_room
from room import Room
from database import DB
from functools import wraps


app = Flask(__name__)

#Secret Key
app.secret_key = "ferias"

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

socketio = SocketIO(app)

rooms = {}
categorias = {}
subcategorias = {}
login = {}


for categoria in DB.getInstance().executeQuery("select id, nome from categorias"):
    categorias.setdefault(categoria[0], str(categoria[1]).capitalize())

for subcategoria in DB.getInstance().executeQuery("select id_categoria, id, nome from subcategorias"):
    if not subcategorias.get(subcategoria[0]):
        subcategorias.setdefault(subcategoria[0], {})

    subcategorias.get(subcategoria[0]).setdefault(subcategoria[1], str(subcategoria[2]).capitalize())


@app.route('/')
def index():
    existing_rooms = []
    total_online = 0

    for room_id in rooms:
        room = rooms[room_id]

        categoria = categorias.get(room.getCategory())
        subcategoria = subcategorias.get(room.getCategory())

        if subcategoria:
            subcategoria = subcategoria.get(room.getSubcategory())

        existing_rooms.append({
            'id': room.getId(),
            'category': categoria,
            'subcategory': subcategoria,
            'players': room.getPlayersCount()
            })

        total_online += room.getPlayersCount()

    return render_template('index.html', total_online=total_online, categorias=categorias, subcategorias=subcategorias, existing_rooms=existing_rooms)

@app.route('/room/<int:room_id>')
def room(room_id):

    room = rooms.get(room_id)

    if(room):
        return render_template('room.html', room_id = room_id, players = room.getPlayers())
    else:
        return "<h1>Error 404 - Not found</h1>"


@app.route('/create_room', methods=['POST'])
def create_room():
    if(len(rooms) == 300):
        return "Full"

    id = 1
    for i  in range(1,300):
        id = i
        if(not rooms.get(id)):
            break

    rooms.setdefault(id, Room(id, int(request.form['category']), int(request.form['subcategory'])))


    return redirect("/room/"+str(id))

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = rooms.get(int(data['room']))

    print(username + ' has entered the room: ' + data['room'])

    #add player and send current drawing
    room = rooms.get(int(data['room']))

    if(not room):
        return

    join_room(int(data['room']))

    room.addPlayer(request.sid, {'username': username, 'points': 0})
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

    if(not room):
        return

    rooms.get(room).addCommand(data)
    print(data)
    emit("invoke method", data, include_self=False, room = room)

#login
@app.route('/login', methods=['GET', 'POST'])
@login_required
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Usuario ou senha nao estao corretos'
        else:
            session['logged_in'] = True
            #redirect for page game
            flash('Jogo acessado com sucesso!')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

#logout
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    #Fazer tela de logout
    flash('Voce deslogo do jogo!')
    return redirect(url_for('index'))

#Debug
if __name__ == '__main__':
    app.run(debug=True)
