class Room extends RemoteObject {

    constructor(protocol, domain, port, room) {
        super(protocol, domain, port, room);

        this.players = [];
        this.observer = true;
    }

    
    
}