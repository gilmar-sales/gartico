import threading
import time
import random
from database import DB
from flask import request

room_list = {}

class Room:
    def __init__(self, socketio, id, category, subcategory):
        self.socketio = socketio
        self.id = id
        
        self.playing = False
        self.players_sid = []

        self.object_ids = []
        self.current_index = 0
        self.current_object = None

        self.correctPlayers = {}

        query="select `id` from `objetos` where `id_categoria` = '{}' and `id_subcategoria` = '{}'".format(category, subcategory)
        for id in DB.getInstance().executeQuery(query):
            self.object_ids.append(id[0])
        
        random.shuffle(self.object_ids)

        self.draw = []
        self.last_action = -1

        self.category = category
        self.subcategory = subcategory

        self.players = {}
        self.currentDrawer = 0
        self.nextRoundTimer = threading.Timer(120.0, self.nextRound, [])

        self.destroyTimer = threading.Timer(15.0, room_list.pop, [self.id])
        self.destroyTimerActive = False

    def getId(self):
        return self.id

    def validateAnswer(self, answer):
        if  self.players_sid[self.currentDrawer] == request.sid:
            return

        status = None
        if not self.current_object:
            status = -1
        elif answer == self.current_object:
            status = 1
        elif self.current_object.find(answer) > -1:
            status = 0
        elif self.current_object.lower().find(answer) > -1:
            status = 0
        else:
            status = -1
        
        if status == 1:
            self.socketio.emit("invoke method", {'method': 'appendAnswer',  'args': [ self.getPlayerName(request.sid), 'acertou!', status]}, include_self=True, room = self.id)
            self.correctPlayers.setdefault(request.sid, True)

            if len(self.correctPlayers) >= len(self.players_sid) - 1:
                self.nextRound()
        elif status == 0:
            self.socketio.emit("invoke method", {'method': 'appendAnswer',  'args': [ self.getPlayerName(request.sid), answer, status]}, include_self=True, room = request.sid)
        else:
            self.socketio.emit("invoke method", {'method': 'appendAnswer',  'args': [ self.getPlayerName(request.sid), answer, status]}, include_self=True, room = self.id)

    def getPlayerName(self, sid):
        return self.players.get(sid)['username']

    def getPlayers(self):
        players = []
        for player in self.players:
            players.append(self.players.get(player)['username'])

        return players

    def getPlayersCount(self):
        return len(self.players)

    def getPlayerByNick(self, nick):
        for index in self.players:
            if self.players.get(index)['username'] == nick:
                return True
        
        return False
    
    def addPlayer(self, sid, data):
        self.players_sid.append(sid)
        self.players.setdefault(sid, data)
        self.socketio.emit('invoke method', {'method': 'addPlayer', 'args': [data]}, room = self.id)
       
        self.destroyTimerActive = False
        self.destroyTimer.cancel()
        self.destroyTimer = threading.Timer(15.0, room_list.pop, [self.id])
    
    def removePlayer(self, player):
        if self.players.get(player):
            self.socketio.emit('invoke method', {'method': 'removePlayer', 'args': [self.players.get(player)['username']]}, room = self.id)
        self.players.pop(player)
        self.players_sid.remove(player)
        
        if not self.getPlayersCount() > 0:
            if not self.destroyTimerActive:
                self.destroyTimerActive = True
                self.destroyTimer.start()

    def nextWord(self):
        query = "select `nome` from `objetos` where `id` = '{}' and `id_categoria` = '{}' and `id_subcategoria` = '{}'".format(self.object_ids[self.current_index], self.category, self.subcategory)
        self.current_index+=1
        
        if(self.current_index >= len(self.object_ids)):
            self.current_index = 0
            random.shuffle(self.object_ids)

        self.current_object = DB.getInstance().executeQuery(query)[0][0]


    def sendCharCount(self, sid):
        counts = []

        for word in self.current_object.split():
            counts.append(len(word))

        self.socketio.emit('invoke method', {'method': 'setCharCount', 'args': [counts]}, room = sid)

    def getCategory(self):
        return self.category
    
    def getSubcategory(self):
        return self.subcategory

    def isPlaying(self):
        return self.playing
    
    def addCommand(self, command):
        if(command['args'][0] == 'clear'):
            self.draw.clear()
            self.last_action = -1
        else:
            self.draw.append(command)

            self.last_action += 1

    def sendDraw(self, player):
        for command in self.draw:
            self.socketio.emit('invoke method', command, room = player)
    
    def start(self):
        self.playing = True
        print("starting game room: {}".format(self.id))
        self.nextWord()
        self.nextRoundTimer.start()
        for i in self.players_sid:
            if(i == self.players_sid[self.currentDrawer]):
                self.socketio.emit('invoke method', {'method': 'setListener', 'args': [False]}, room = i)
                self.socketio.emit('invoke method', {'method': 'setObject', 'args': [self.current_object]}, room = i)
            else:
                self.socketio.emit('invoke method', {'method': 'setListener', 'args': [True]}, room = i)
                self.sendCharCount(i)
                
            self.socketio.emit('invoke method', {'method': 'setCountDown', 'args': [120]}, room = i)
            self.socketio.emit('invoke method', {'method': 'start', 'args': []}, room = i)
    
    def stop(self):
        self.playing = False
        self.nextRoundTimer.cancel()
        self.nextRoundTimer = threading.Timer(120.0, self.nextRound, [])
        print("stoping game room: {}".format(self.id))
        self.socketio.emit('invoke method', {'method': 'stop', 'args': []}, room = self.id)

    def nextRound(self):
        if(self.currentDrawer < len(self.players_sid) - 1):
            self.currentDrawer += 1
        else:
            self.currentDrawer =0

        self.stop()
        self.start()
