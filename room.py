class Room:
    def __init__(self, id):
        self.id = id
        self.draw = []
        self.players = []
        self.currentDrawer = 0
        self.playing = False 
        self.last_action = -1

    def getPlayersCount(self):
        return len(self.players)

    def isPlaying(self):
        return self.playing
    
    def addPlayer(self, player):
        self.players.append(player)
        print('the room ' + str(self.id) + ' now have ' + str(self.getPlayersCount()) + ' players!')
    
    def removePlayer(self, player):
        self.players.remove(player)
        print('the room ' + str(self.id) + ' now have ' + str(self.getPlayersCount()) + ' players!')
        return not self.getPlayersCount() > 0
    
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