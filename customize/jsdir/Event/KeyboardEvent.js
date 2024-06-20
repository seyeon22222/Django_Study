export class KeyboardEvent {
    static message = null;
    static flag = 0;
    
    constructor(type, cam) {
        this.type = null;
        this.k_event = null;
        if (type === 'keyup')
            this.setKeyUp(cam);
        if (type === 'keydown')
            this.setKeyDown(cam);
    }

    destructor() {
        window.removeEventListener(this.type, this.k_event);
    }

    setKeyUp(cam) {
        let tmp_event = (event) => {
            if (event.code === "KeyQ") {
                KeyboardEvent.message = { message: "1pupstop", players: Main.players, uuid: "" };
                KeyboardEvent.flag = 1;
              }
              if (event.code == "KeyA") {
                KeyboardEvent.message = { message: "1pdownstop", players: Main.players, uuid: "" };
                KeyboardEvent.flag = 1;
              }
              if (event.code === "KeyO") {
                KeyboardEvent.message = { message: "2pupstop", players: Main.players, uuid: "" };
                KeyboardEvent.flag = 1;
              }
              if (event.code === "KeyL") {
                KeyboardEvent.message = { message: "2pdownstop", players: Main.players, uuid: "" };
                KeyboardEvent.flag = 1;
              }
              if (event.code === "ArrowRight" || event.code === "ArrowLeft")
                cam.rotCam(0);
        }
        window.addEventListener('keyup', tmp_event);
        this.type = 'keyup';
        this.k_event = tmp_event;
    }

    setKeyDown(cam) {
        let tmp_event = (event) => {
            if (event.code === "KeyQ") {
                KeyboardEvent.message = { message: "1pup", players: Main.players, uuid: "" };
                KeyboardEvent.flag = 1;
            }
            if (event.code === "KeyA") {
                KeyboardEvent.message = { message: "1pdown", players: Main.players, uuid: "" };
                KeyboardEvent.flag = 1;
            }
            if (event.code === "KeyO") {
                KeyboardEvent.message = { message: "2pup", players: Main.players, uuid: "" };
                KeyboardEvent.flag = 1;
            }
            if (event.code === "KeyL") {
                KeyboardEvent.message = { message: "2pdown", players: Main.players, uuid: "" };
                KeyboardEvent.flag = 1;
            }
            if (event.code === "ArrowRight")
                cam.degree = Math.min(45, cam.degree + 1);
            if (event.code === "ArrowLeft")
                cam.degree = Math.max(-45, cam.degree - 1);
            cam.rotCam(cam.degree);
        }
        window.addEventListener('keydown', tmp_event);
        this.type = 'keydown';
        this.k_event = tmp_event;
    }
}