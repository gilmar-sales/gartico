class RemoteObject {
    static socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    static handler = {
        apply: function(target, thisArg, argumentsList) {
          console.log(`request: ${argumentsList}`);
          RemoteObject.socket.emit("request rmi", {...argumentsList});
          return target(...argumentsList);
        }
    };

    constructor() {
        RemoteObject.socket.on('connect', () => {
            console.log(typeof(this) + " connected to the server");
        });

        // When a new vote is announced, add to the unordered list
        RemoteObject.socket.on('invoke method' , data => {
            alert(data);
            if(this.__proto__['print'])
                console.log("metodo encontrado");
        });

        // Make request for each method apply
        var current = this.__proto__;
        console.log(this.constructor.name);


        Object.getOwnPropertyNames(current).forEach((name) => {
            if (typeof current[name] === 'function') {
                current[name] = new Proxy(current[name], RemoteObject.handler);
            }
        });
    };
}

class SVGCanvas extends RemoteObject {

    static tools = {
        pen: 1,
        pencil: 2,
        eraser: 3
    };
    
    tool = SVGCanvas.tools.pen;

    constructor(svg) {
        super();
        
        this.svg = d3.select(svg);
    }

    print(text) {
        console.log(text);
    }

    draw_point(x, y, connect) {

        const color = this.tool == SVGCanvas.tools.eraser ? 'white' : 'black';
        const thickness = 5;

        if (connect) {
            const last_point = points[points.length - 1];
            const line = svg.append('line')
                            .attr('x1', last_point.attr('cx'))
                            .attr('y1', last_point.attr('cy'))
                            .attr('x2', x)
                            .attr('y2', y)
                            .attr('stroke-width', thickness * 2)
                            .style('stroke', color);
            lines.push(line);
        }

        const point = svg.append('circle')
                            .attr('cx', x)
                            .attr('cy', y)
                            .attr('r', thickness)
                            .style('fill', color);
        points.push(point);
    }

    clear() {
        for (let i = 0; i < points.length; i++)
            points[i].remove();
        for (let i = 0; i < lines.length; i++)
            lines[i].remove();
        points = [];
        lines = [];
    }
}

document.addEventListener('DOMContentLoaded', () => {
    
    let remote = new SVGCanvas('#svg');

    remote.print("teste");
    console.log(remote);

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {

        document.querySelector('#clear').onclick = () => {
            socket.emit('request command', 'clear');
        };
    });

    // When a new vote is announced, add to the unordered list
    socket.on('send circle', data => {
        draw_point(data['x'], data['y'], data['connect']);
    });

    socket.on('send command', data => {
        alert(data);
    });

    
// state
let draw = false;

let tools = {
    pen: 1,
    pencil: 2,
    eraser: 3
};

let tool = tools.pen;

// elements
let points = [];
let lines = [];

let action_point = [];
let action_line = [];

let svg = null;


function selectTool(selectedTool) {
    tool = selectedTool;
}

function render() {
    // create the selection area
    svg = d3.select('#svg');


    svg.on('mousedown', function() {
        draw = true;
        const coords = d3.mouse(this);
        draw_point(coords[0], coords[1], false);
        action_line.push(lines.length-1);
        action_point.push(points.length-1);
        socket.emit("draw circle", {'x': coords[0], 'y': coords[1], 'connect': false});
    });

    svg.on('mouseup', () =>{
        draw = false;

    });

    svg.on('mousemove', function() {
        if (!draw)
            return;
        const coords = d3.mouse(this);
        draw_point(coords[0], coords[1], true);
        socket.emit("draw circle", {'x': coords[0], 'y': coords[1], 'connect': true});
    });

    document.onkeydown = (ev) => {
        if(ev.ctrlKey && ev.key == "z") {
            document.querySelector('#undo').onclick();
        }
    }

    document.onkeyup = (ev) => {

    }

    document.querySelector('#clear').onclick = () => {

        socket.emit("request command", {'x': coords[0], 'y': coords[1], 'connect': true});

        for (let i = 0; i < points.length; i++)
            points[i].remove();
        for (let i = 0; i < lines.length; i++)
            lines[i].remove();
        points = [];
        lines = [];
    }

    document.querySelector('#undo').onclick = () => {
        last_action_point = action_point.length-1;
        last_action_line = action_line.length-1;

        for(let i = points.length - 1;last_action_line >= 0 && i >= action_point[last_action_point]; i--)
            points[i].remove();
        for(let i = lines.length - 1;last_action_line >= 0 && i > action_line[last_action_line]; i--)
            lines[i].remove();

        action_point.pop(last_action_point);
        action_line.pop(last_action_line);
    }

}

function draw_point(x, y, connect) {

    const color = tool == tools.eraser ? 'white' : 'black';
    const thickness = 5;

    if (connect) {
        const last_point = points[points.length - 1];
        const line = svg.append('line')
                        .attr('x1', last_point.attr('cx'))
                        .attr('y1', last_point.attr('cy'))
                        .attr('x2', x)
                        .attr('y2', y)
                        .attr('stroke-width', thickness * 2)
                        .style('stroke', color);
        lines.push(line);
    }

    const point = svg.append('circle')
                        .attr('cx', x)
                        .attr('cy', y)
                        .attr('r', thickness)
                        .style('fill', color);
    points.push(point);
}

render();

});
