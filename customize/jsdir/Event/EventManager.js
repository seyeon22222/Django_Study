import { MouseEvent } from "./MouseEvent.js";

export class EventManager {
    static event_list = [];
    static list_size = 0;

    static setEventMouse(ray, button, objects) {
        EventManager.event_list.push(new MouseEvent("click", ray, button, objects));
        EventManager.event_list.push(new MouseEvent('mousemove', ray));
        EventManager.event_list.push(new MouseEvent('mouseup'));
        EventManager.event_list.push(new MouseEvent('mousedown', ray));
        EventManager.list_size += 4;
    }

    static addEventKeyboard(type) {

    }

    static subEvent(idx) {
        window.removeEventListener(EventManager.event_list[idx].type, EventManager.event_list[idx]);
        EventManager.event_list.splice(idx, 1);
        EventManager.list_size -= 1;
    }
};