// The handler to make the proxy emit the request of the method
const handler = {
  apply: function (target, thisArg, argumentsList) {
    if (thisArg.listener) return;

    thisArg.socket.emit("request invoke", {
      room: thisArg.room,
      method: target.name,
      args: argumentsList,
    });

    return target.apply(thisArg, argumentsList);
  },
};

class RemoteObject {
  constructor(protocol, domain, port, room, join) {
    this.socket = io.connect(protocol + "//" + domain + ":" + port);
    this.room = room;
    this.listener = true;

    // Backup of the methods that cannot be accessed throught the proxy
    this.__targets__ = [];

    //
    this.socket.on("connect", () => {
      this.socket.emit("join", { room: this.room, join: join });

      window.addEventListener("beforeunload", (ev) => {
        this.socket.emit("leave", { room: this.room });
        (ev || window.event).returnValue = "Tem certeza que deseja sair?";
        (ev || window.event).preventDefault();
      });
    });

    this.socket.on("check", () => {
      this.socket.emit("check", { room: this.room });
    });

    // When a request is called by the server, apply the method
    this.socket.on("invoke method", (data) => {
      if (this.__targets__[data["method"]])
        this.__targets__[data["method"]].apply(this, data["args"]);
    });

    // Make the proxy for each method apply
    var current = this.__proto__;

    while (current["constructor"]["name"] != "Object") {
      Object.getOwnPropertyNames(current).forEach((name) => {
        this.__targets__[name] = current[name];
        if (typeof current[name] === "function") {
          current[name] = new Proxy(current[name], handler);
        }
      });

      current = current.__proto__;
    }
  }

  setListener(value) {
    this.listener = value;
  }
}
