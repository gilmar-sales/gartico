from flask_socketio import SocketIO
from server.app import app

socketio = SocketIO(app)