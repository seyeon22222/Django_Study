import { MouseEvent } from "./MouseEvent.js";
import { KeyboardEvent } from "./KeyboardEvent.js";

export class EventManager {
    static mouse_list = [];
    static key_list = [];

    static setEventMouse(ray, button, objects) {
        EventManager.mouse_list.push(new MouseEvent('click', ray, button, objects));
        EventManager.mouse_list.push(new MouseEvent('mousemove', ray));
        EventManager.mouse_list.push(new MouseEvent('mouseup', null, null, objects));
        EventManager.mouse_list.push(new MouseEvent('mousedown', ray));
        EventManager.mouse_list.push(new MouseEvent('start', null, null, objects));
    }

    static setEventKeyboard(cam) {
        EventManager.key_list.push(new KeyboardEvent('keydown', cam));
        EventManager.key_list.push(new KeyboardEvent('keyup', cam));
    }

    static deleteEvent(type) {
        if (type === 'mouse') {
            for (let i = 0; i < EventManager.mouse_list.length; i++)
                EventManager.mouse_list[i].destructor();
            EventManager.mouse_list = [];
        }
        else if (type === 'keyboard'){
            for (let i = 0; i < EventManager.key_list.length; i++)
                EventManager.key_list[i].destructor();
            EventManager.key_list = [];
        }
    }
};