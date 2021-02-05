import os
from flask import render_template, request, redirect, url_for, session, flash
from flask_socketio import emit, join_room, leave_room
from server.room import room_list, Room
from server.database import DB
from server.account_controller import AccountController
from server.app import app
from server.socketio import socketio

acc = AccountController()

categorias = {}
subcategorias = {}


for categoria in DB.getInstance().executeQuery("select id, nome from categorias"):
    categorias.setdefault(categoria[0], str(categoria[1]).capitalize())

for subcategoria in DB.getInstance().executeQuery("select id_categoria, id, nome from subcategorias"):
    if not subcategorias.get(subcategoria[0]):
        subcategorias.setdefault(subcategoria[0], {})

    subcategorias.get(subcategoria[0]).setdefault(subcategoria[1], str(subcategoria[2]).capitalize())

sid_list = {}

@app.route('/')
def index():
    existing_rooms = []
    total_online = 0

    for room_id in room_list:
        room = room_list[room_id]

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
@acc.login_required
def room(room_id):

    room = room_list.get(room_id)

    if(room):
        if room.getPlayerByNick(session['nickname']): #TODO: reconnect
            return redirect(url_for('index'))
        else:
            return render_template('room.html', room_id = room_id, players = room.getPlayers())
    else:
        return redirect(url_for('index'))


@app.route('/create_room', methods=['POST'])
@acc.login_required
def create_room():
    if(len(room_list) == 300):
        return "Full"

    id = 1
    for i  in range(1,300):
        id = i
        if(not room_list.get(id)):
            break

    room_list.setdefault(id, Room(id, int(request.form['category']), int(request.form['subcategory'])))

    return redirect("/room/"+str(id))

@socketio.on('connect')
def connect():
    print(f"{session['nickname']} ({request.sid})  connected")

@socketio.on('disconnect')
def disconnect():
    sid_data = sid_list.get(request.sid)
    room = room_list.get(int(sid_data['room']))

    #update server room_list
    if room:
        room.removePlayer(request.sid)

    sid_list.pop(request.sid)
    print(request.sid + " disconnected")

@socketio.on('join')
def on_join(data):
    username = session['nickname']
    join_room(int(data['room']))

    room = room_list.get(int(data['room']))
    if room:
        #add player and send current drawing
        print(username + ' has entered the room: ' + data['room'])

        sid_list.setdefault(request.sid, {'username': username, 'room': data['room']})

        room.addPlayer(request.sid, {'username': username, 'points': 0})
        room.sendDraw(request.sid)

        #start game with 2 or more players
        if(room.getPlayersCount() > 1 and not room.isPlaying()):
            room.start()

@socketio.on('leave')
def on_leave(data):
    room = room_list.get(int(data['room']))

    leave_room(data['room'])

    #update server room_list
    if room:
        room.removePlayer(request.sid)

# response to remote object call
@socketio.on("request invoke")
def invoke(data):
    room = room_list.get(int(data['room']))

    if(room):
            room.addCommand(data)    

    emit("invoke method", data, include_self=False, room = int(data['room']))

@socketio.on("sendAnswer")
def sendAnswer(data):
    room = room_list.get(int(data['room']))

    if(room):
        room.sendAnswer(data['answer'])

@socketio.on("sendMessage")
def sendMessage(data):
    room = room_list.get(int(data['room']))

    if(room):
        room.sendMessage(data['message'])

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = DB.getInstance().validateInput(request.form['username'])
        password = DB.getInstance().validateInput(request.form['password'])

        query = "select `id`, `nickname` from `usuarios` where `login` = '{}' and `senha` = MD5('{}')".format(username, password)
        results = DB.getInstance().executeQuery(query)
        
        if not len(results):
            error = 'Usuário ou senha incorretos'
        else:
            session['logged_in'] = True
            session['nickname'] = results[0][1]
            #redirect for page game
            flash('Jogo acessado com sucesso!')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

#logout
@app.route('/logout')
@acc.login_required
def logout():
    session.pop('logged_in', None)
    session.pop('nickname', None)
    
    return redirect(url_for('index'))

@app.route('/register', methods=["GET", "POST"])
def register():
    error = None
    success = None

    if request.method == "POST":
        login = DB.getInstance().validateInput(request.form['username'])
        password = DB.getInstance().validateInput(request.form['password'])
        nick = DB.getInstance().validateInput(request.form['nickname'])

        check_login_query = "select `id` from `usuarios` where `login` = '{}'".format(login)
        check_nick_query = "select `id` from `usuarios` where `nickname` = '{}'".format(nick)
        if not nick:
            error = "Apelido inválido"
        elif len(nick) < 5:
            error = "O apelido deve conter pelo menos 5 caracteres"
        if not login:
            error = "Login inválido"
        elif len(login) < 5:
            error = "O login deve conter pelo menos 5 caracteres"
        elif not password:
            error = "Senha inválida"
        elif len(password) < 8:
            error = "A senha deve conter pelo menos 8 caracteres"
        elif len(DB.getInstance().executeQuery(check_login_query)):
            error = "Nome de usuário indisponível"
        elif len(DB.getInstance().executeQuery(check_nick_query)):
            error = "Apelido indisponível"
        else:
            query = "insert into `usuarios` (`login`, `senha`, `nickname`) values('{}', MD5('{}'), '{}')".format(login, password, nick)
            DB.getInstance().executeQuery(query)
            DB.getInstance().apply()
            success = True

    return render_template('register.html', error=error, success=success)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
