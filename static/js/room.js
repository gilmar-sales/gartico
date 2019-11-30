class Room extends RemoteObject {

    constructor(svg, protocol, domain, port, room) {
        super(protocol, domain, port, room);

        this.observer = true;
        this.canvas = new SVGCanvas(svg);
    }

    callCanvas(method, ...params) {
            return this.canvas[method](...params);
    }
    
}