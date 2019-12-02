class RemoteObject {
    // The handler to make the proxy emit the request of the method 
    static handler = {
        apply: function(target, thisArg, argumentsList) {
            if(thisArg.listener)
                return;
            thisArg.socket.emit("request invoke", {room: thisArg.room, packet: thisArg.actual_packet++, method: target.name, args: argumentsList});

            return target.apply(thisArg, argumentsList);
        }
    };

    constructor(protocol, domain, port, room) {
        this.socket = io.connect(protocol + '//' + domain + ':' + port);
        this.room = room;
        this.listener = false;

        //tcp protocol
        this.packets = {};
        this.processed_packet = 0;
        
        this.actual_packet = 0; // number of the last packet processed
        // Backup of the methods that cannot be accessed throught the proxy
        this.__targets__ = [];

        //
        this.socket.on('connect', () => {
            this.socket.emit('join', {room: room});
            
            window.onbeforeunload = () => {
                this.socket.emit('leave', {room: room});
            }
        });

        // When a request is called by the server, apply the method
        this.socket.on('invoke method' , data => {
            
            if(data['packet'] > this.processed_packet) {
                this.packets[data['packet']] = data;
                console.log("armazenando pacote: " + data['packet']+ " atual: " + this.processed_packet);
            }
            else {
                for(const packet in this.packets) {
                    if(packet > this.processed_packet)
                        break;

                    this.__targets__[this.packets[packet]['method']].apply(this, this.packets[packet]['args']);
                    this.processed_packet++;
                    this.actual_packet++;
                    delete this.packets[packet];
                    console.log("aplicando pacote");
                }

                console.log("aplicando pacote");

                if(this.__targets__[data['method']])
                    this.__targets__[data['method']].apply(this, data['args']);
                
                this.processed_packet++;
                this.actual_packet++;

            }
        });

        // Make the proxy for each method apply
        var current = this.__proto__;

        while(current['constructor']['name'] != "Object") {
            Object.getOwnPropertyNames(current).forEach((name) => {
                this.__targets__[name] = current[name];
                if (typeof current[name] === 'function') {
                    current[name] = new Proxy(current[name], RemoteObject.handler);
                }
            });
            
            current = current.__proto__;
        }
    }

    setListener(value) {
        this.listener = value;
    }
}
