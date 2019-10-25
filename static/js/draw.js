class Rectangle {
    constructor(svg, thickness, color) {
        this.data = null;
        this.svg = svg;
        this.thickness = thickness;
        this.color = color;
    }

    draw(x, y, shiftKey = false) {
        if(this.data == null) {
            this.data = this.svg.append('rect')
                .attr('x', x)
                .attr('y', y)
                .style('fill', 'transparent')
                .style('stroke-width', this.thickness * 2)
                .style('stroke', this.color);
            
            this.x = x;
            this.y = y;
        } else {
            if(shiftKey) {
                this.data 
                .attr('width', Math.abs( x - this.data.attr("x")))
                .attr('height', Math.abs( x - this.data.attr("x")))
            } else {
                
                if(x - this.x < 0) {
                    this.data 
                    .attr('x', this.x - (this.x - x));
                }

                if(y - this.y < 0) {
                    this.data 
                    .attr('y', this.y - (this.y - y));
                }
                
                this.data 
                    .attr('width', Math.abs( x - this.x)) 
                    .attr('height', Math.abs( y - this.y));
            }
        }
    }
    
    show() {
        this.data
            .style('fill', 'transparent')
            .style('stroke', this.color);
    }

    hide() {
        this.data
            .style('fill', 'transparent')
            .style('stroke', 'transparent');
    }

    clear() {
        this.data.remove();
    }
    
}

class Ellipse {
    constructor(svg, thickness, color) {
        this.data = null;
        this.svg = svg;
        this.thickness = thickness;
        this.color = color;
    }

    draw(x,y, shiftKey = false) {
        if(this.data == null) {
            this.data = this.svg.append('ellipse')
                .attr('cx', x)
                .attr('cy', y)
                .style('fill', 'transparent')
                .style('stroke-width', this.thickness * 2)
                .style('stroke', this.color);
        } else {
            if(shiftKey) {
                this.data 
                .attr('rx', Math.abs( x - this.data.attr("cx")))
                .attr('ry', Math.abs( x - this.data.attr("cx")))
            } else {
                this.data 
                .attr('rx', Math.abs( x - this.data.attr("cx")))
                .attr('ry', Math.abs( y - this.data.attr("cy")));
            }
        }
    }

    show() {
        this.data
            .style('fill', 'transparent')
            .style('stroke', this.color);
    }

    hide() {
        this.data
            .style('fill', 'transparent')
            .style('stroke', 'transparent');
    }

    clear() {
        this.data.remove();
    }
    
}

class Triangle {
    constructor(svg, thickness, color) {
        this.svg = svg;
        this.thickness = thickness;
        this.color = color;

        this.data = null;
    }

    draw(x, y, shiftKey = false) {
        if(this.data == null) {
            this.data = this.svg.append('polygon')
                .attr('points', [x,y].join())
                .style('fill', 'transparent')
                .style('stroke', this.color)
                .style('stroke-width', this.thickness * 2);
                this.x = x;
                this.y = y;
        } else {
            if(shiftKey)
            this.data
                .attr('points', [this.x + (x - this.x)/2, this.y].join() + " " + [this.x, this.y + (x - this.x)].join() + " " + [x, this.y + (x - this.x)].join());
            else
            this.data
                .attr('points', [this.x + (x - this.x)/2, this.y].join() + " " + [this.x, y].join() + " " + [x,y].join());
        }
    }
    
    show() {
        this.data
            .style('fill', 'transparent')
            .style('stroke', this.color);
    }

    hide() {
        this.data
            .style('fill', 'transparent')
            .style('stroke', 'transparent');
    }

    clear() {
        this.data.remove();
    }
}

class Stroke {
    constructor(svg, thickness, color) {
        this.svg = svg;
        this.thickness = thickness;
        this.color = color;
        this.data = [];
        this.last_action = -1;
    }

    draw(x, y) {
        if(this.data.length > 0) {
            var last = this.data[this.data.length -1];
            const line = this.svg.append('line')
                .attr('x1', last.attr('cx'))
                .attr('y1', last.attr('cy'))
                .attr('x2', x)
                .attr('y2', y)
                .attr('stroke-width', this.thickness * 2)
                .style('stroke', this.color)
                .on("mouseover", () => {
                    this.onMouseOver();
                });

            this.data.push(line);
        }

        let point = this.svg.append('circle')
            .attr('cx', x)
            .attr('cy', y)
            .attr('r', this.thickness)
            .style('fill', this.color);

        point.parent = this;
        this.data.push(point);
    }

    show() {
        this.data.forEach(stroke => {
            stroke
            .style('stroke', this.color)
            .style('fill', this.color);
        });
    }

    hide() {
        this.data.forEach(stroke => {
            stroke
            .style('stroke', 'transparent')
            .style('fill', 'transparent');
        });
    }

    clear() {
        this.data.forEach(stroke => {
            stroke.remove();
        });
    }

    onMouseOver() {
        this.data.forEach(stroke => {
            stroke.attr({
                fill: "orange",
                r: this.thickness * 2.5
              });
        });
    }

    onMouseOut() {
        this.parent.parentdata.forEach(stroke => {
            stroke.attr({
                fill: this.parent.color,
                r: this.parent.thickness * 2
              });
        });
    }
    
}

class SVGCanvas extends RemoteObject {

    static tools = {
        pen: 1,
        pencil: 2,
        eraser: 3,
        rectangle: 4,
        ellipse: 5,
        triangle: 6
    }

    constructor(svg, protocol, domain, port, room) {
        super(protocol, domain, port, room);
        
        this.svg = d3.select(svg);
        this.tool = SVGCanvas.tools.pen;

        this.drawing = false;
        this.shiftKey = false;
        this.color = '#000000';
    
        // elements
        this.data = [];
        this.current_draw = null;
        this.last_action = -1;
    }

    setTool(tool) {
        this.tool = SVGCanvas.tools[tool];
    }

    setDrawing(drawing) {
        this.drawing = drawing;
    }

    setColor(color) {
        this.color = color;
    }

    draw(x, y) {
        if(!this.drawing) { //starts a new draw
            for(let i = this.data.length - 1; i > this.last_action; i--) {
                this.data[i].clear();
                this.data.pop();
            }

            switch (this.tool) {
                case SVGCanvas.tools.pen:
                    this.current_draw = new Stroke(this.svg, 5, this.color);
                    this.current_draw.draw(x, y);
                break;
                case SVGCanvas.tools.rectangle:
                    this.current_draw = new Rectangle(this.svg, 5, this.color);
                    this.current_draw.draw(x,y);
                break;
                case SVGCanvas.tools.ellipse:
                    this.current_draw = new Ellipse(this.svg, 5, this.color);
                    this.current_draw.draw(x,y);
                break;
                case SVGCanvas.tools.triangle:
                    this.current_draw = new Triangle(this.svg, 5, this.color);
                    this.current_draw.draw(x,y);
                break;
                default:
                    break;
            }

            this.data.push(this.current_draw);
            this.last_action++;
            this.setDrawing(true);
        } else {
            switch (remote.tool) {
                case SVGCanvas.tools.pen :
                    this.current_draw.draw(x, y);
                    break;
                case SVGCanvas.tools.eraser :
                    this.current_draw.draw(x, y);
                    break;
                case SVGCanvas.tools.rectangle:
                        this.current_draw.draw(x, y, this.shiftKey);
                    break;
                case SVGCanvas.tools.ellipse:
                        this.current_draw.draw(x, y, this.shiftKey);
                    break;
                    case SVGCanvas.tools.triangle:
                            this.current_draw.draw(x, y, this.shiftKey);
                        break;
                default:
                    break;
            }
        }
    }

    clear() {
        this.data.forEach(draw => {
            draw.clear();
        });

        this.data = [];
        this.last_action = -1;
    }

    undo() {
        if(this.last_action >= 0) {
            var last_draw = this.data[this.last_action];
            

            last_draw.hide();
            this.last_action--;
        }
    }

    redo() {
        if(this.last_action < this.data.length -1) {
            var last_draw = this.data[this.last_action+1];
            

            last_draw.show();
            this.last_action++;
        }
    }
}

