from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/room/<int:room_id>')
def room(room_id):
    return render_template('room.html', room_id = room_id)