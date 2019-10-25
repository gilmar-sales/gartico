class RemoteObject {
    // The handler to make the proxy emit the request of the method 
    static handler = {
        apply: function(target, thisArg, argumentsList) {
            if(thisArg.observer)
                return;
            thisArg.socket.emit("request invoke", {room: thisArg.room, method: target.name, args: argumentsList});

            return target.apply(thisArg, argumentsList);
        }
    };

    constructor(protocol, domain, port, room) {
        this.socket = io.connect(protocol + '//' + domain + ':' + port);
        this.room = room;
        this.observer = false;

        // Backup of the methods that cannot be accessed throught the proxy
        this.__targets__ = [];

        //
        this.socket.on('connect', () => {
            this.socket.emit('join', {username: 'gilmar', room: room});
        });

        // When a request is called by the server, apply the method
        this.socket.on('invoke method' , data => {
            if(this.__targets__[data['method']])
                this.__targets__[data['method']].apply(this, data['args']);
        });

        // Make the proxy for each method apply
        var current = this.__proto__;

        Object.getOwnPropertyNames(current).forEach((name) => {
            this.__targets__[name] = current[name];
            if (typeof current[name] === 'function') {
                current[name] = new Proxy(current[name], RemoteObject.handler);
            }
        });
    };
}

class RemoteInvocator {
    // The handler to make the proxy emit the request of the method invocation
    static handler = {
        apply: function(target, thisArg, argumentsList) {
            thisArg.socket.emit("request invoke", {room: thisArg.room, method: target.name, args: argumentsList});

            return target.apply(thisArg, argumentsList);
        }
    };
    
    constructor(protocol, domain, port, room) {
        this.socket = io.connect(protocol + '//' + domain + ':' + port);
        this.room = room;

        // On connect join the socketIO room
        this.socket.on('connect', () => {
            this.socket.emit('join', {username: 'gilmar', room: room});
        });

        
        // Backup of the methods that cannot be accessed throught the proxy
        this.__targets__ = [];

        // Make the proxy for each method apply
        var current = this.__proto__;

        Object.getOwnPropertyNames(current).forEach((name) => {
            this.__targets__[name] = current[name];
            if (typeof current[name] === 'function') {
                current[name] = new Proxy(current[name], RemoteInvocator.handler);
            }
        });
    }

}

class RemoteListener {
    constructor(protocol, domain, port, room) {
        this.socket = io.connect(protocol + '//' + domain + ':' + port);
        this.room = room;

        // Backup of the methods that cannot be accessed throught the proxy
        this.__targets__ = [];

        // On connect join the socketIO room
        this.socket.on('connect', () => {
            this.socket.emit('join', {username: 'gilmar', room: room});
        });

        // When a request is called by the server, apply the method
        this.socket.on('invoke method' , data => {
            if(this.__proto__[data['method']])
                this.__proto__[data['method']].apply(this, data['args']);
        });
    }   
}