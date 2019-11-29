class Room:
    def __init__(self, id, category, subcategory):
        self.id = id
        self.playing = False 

        self.draw = []
        self.last_action = -1

        self.category = category
        self.subcategory = subcategory

        self.players = {}
        self.currentDrawer = 0

    def getId(self):
        return self.id

    def getPlayers(self):
        players = []
        for player in self.players:
            players.append(self.players.get(player)['username'])

        return players

    def getPlayersCount(self):
        return len(self.players)
    
    def addPlayer(self, sid, data):
        self.players.setdefault(sid, data)
        print('the room ' + str(self.id) + ' now have ' + str(self.getPlayersCount()) + ' players!')
    
    def removePlayer(self, player):
        self.players.pop(player)
        print('the room ' + str(self.id) + ' now have ' + str(self.getPlayersCount()) + ' players!')
        return not self.getPlayersCount() > 0

    def getCategory(self):
        return self.category
    
    def getSubcategory(self):
        return self.subcategory

    def isPlaying(self):
        return self.playing
    
    def addCommand(self, command):
        if(command['method'] == 'clear'):
            self.draw.clear()
            self.last_action = -1
        else:
            self.draw.append(command)

            self.last_action += 1


    def sendDraw(self, socketio, player):
        for command in self.draw:
             socketio.emit('invoke method', command, room = player)