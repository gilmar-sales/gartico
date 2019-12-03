class Room extends RemoteObject {

    constructor(svg, protocol, domain, port, room) {
        super(protocol, domain, port, room);

        this.observer = true;
        this.canvas = new SVGCanvas(svg);
        this.charCount = 0;
        this.tip = ""
        this.drawer = false;
        this.countDown = 0;
    }

    callCanvas(method, ...params) {
        if(method == 'clear'){ 
            this.actual_packet = 0;
            this.processed_packet = -1;
            this.packets = {}
        }
            
        return this.canvas[method](...params);
    }
    
    start() {
        this.actual_packet = 0;
        this.processed_packet = -1;
        this.packets = {};
        this.canvas.clear();
    }

    stop() {
        document.getElementById("tips").innerHTML = "Aguardando jogadores";
    }

    setCountDown(countDown) {
        this.countDown = countDown;
        console.log(countDown);
    }

    getCountDown() {
        return this.countDown;
    }

    addPlayer(data) {
        var newPlayer = document.createElement('li');
        newPlayer.id = data['username']
        newPlayer.classList.add("row");
        var img = document.createElement('img')
        img.classList.add("user-img")
        img.src = "/static/img/icon-user-default.png"
        var div = document.createElement('div');
        div.classList.add("col");
        var name = document.createElement('a');
        name.classList.add('user-name')
        name.innerHTML = data['username'];
        var points = document.createElement('a');
        points.classList.add('user-rank')
        points.innerHTML = "0pts"

        newPlayer.append(img);
        div.append(name);
        div.append(points);
        newPlayer.append(div);

        document.getElementById("players").append(newPlayer);
    }

    setDrawer(value) {
        this.drawer = value;
    }

    appendAnswer(playerName, answer, status) {
    var container = document.createElement("span");
    var text = document.createTextNode(playerName + ": " + answer);

    container.appendChild(text);
    
    console.log(text);

    if(status == -1)
        container.style.color = "red";
    else if(status == 0)
        container.style.color = "#ff7b00";
    else if(status == 1) {
        container.style.color = "green";
    }

    document.getElementById("answers-area").appendChild(container);
    document.getElementById("answers-area").appendChild(document.createElement("br"));
    
    document.getElementById("answers-area").scrollTo(0, document.getElementById("answers-area").scrollHeight)
    }

    sendTip() {
        
    }

    removePlayer(nickname) {
        document.getElementById(nickname).remove();
    }

    setCharCount(counts) {
        this.charCount = 0;
        var tip = '';

        for (let i in counts) {
            this.charCount += counts[i]
            for (let j = 0; j < counts[i]; j++) {
                this.tip +='_'
                tip += '_ ';
            }
            
            tip += '<br>'
            tip += ' '
        }
        console.log(tip)
        document.getElementById("tips").innerHTML = tip;
    }

    setObject(object) {
        document.getElementById("tips").innerHTML = object;
    }

}