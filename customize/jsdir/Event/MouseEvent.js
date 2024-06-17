import { Pipeline } from "../graphics/Pipeline.js";
import { Box } from "../graphics/Box.js";
import { Mat4 } from "../graphics/Mat4.js";

export class MouseEvent {
    static new_object = null;
    static m_flag = 0;
    static c_flag = 0;
    static cor_x = 0;
    static cor_y = 0;

    static createObject(objects) {
		objects.push(new Box(Pipeline.gl));
		objects[objects.length - 1].createBox(1, 1);
		MouseEvent.new_object = objects[objects.length - 1];
		let loc = Pipeline.gl.getUniformLocation(Pipeline.program.id, "model");
		MouseEvent.new_object.setModelLoc(loc);
    }

    constructor(type, ray = null, button = null, objects = null) {
        this.type = type;
        this.m_event = null;
        if (type == 'click')
            this.setClick(ray, button, objects);
        else if (type == 'mousemove')
            this.setMove(ray);
        else if (type == 'mousedown')
            this.setDown(ray);
        else if (type == 'mouseup')
            this.setUp(ray);
    }

    setClick(ray, button, objects) {
        let tmp_event = (event) => {
            ray.setRay(event.clientX, event.clientY);
            if(MouseEvent.new_object === null && button.collisionRay(ray.ray_des))
                MouseEvent.createObject(objects);
        }
        window.addEventListener('click', tmp_event);
        this.m_event = tmp_event;
    }

    setMove(ray) {
        let tmp_event = (event) => {
            if (MouseEvent.new_object === null)
                return;
            ray.setRay(event.clientX, event.clientY);
            if (MouseEvent.m_flag) {
                if (MouseEvent.c_flag === 0) {
                    let correction = Mat4.sub(ray.ray_des, MouseEvent.new_object.pos);
                    MouseEvent.cor_x = correction[0];
                    MouseEvent.cor_y = correction[1];
                    MouseEvent.c_flag = 1;
                }
                let mov = [ray.ray_des[0] - MouseEvent.cor_x, ray.ray_des[1] - MouseEvent.cor_y, 0];
                MouseEvent.new_object.movePos(mov);
            }
        }
        window.addEventListener('mousemove', tmp_event);
        this.m_event = tmp_event;
    }

    setDown(ray) {
        let tmp_event = (event) => {
            if (MouseEvent.new_object == null || MouseEvent.m_flag === 1)
                return;
            ray.setRay(event.clientX, event.clientY);
            if (MouseEvent.new_object.collisionRay(ray.ray_des))
                MouseEvent.m_flag = 1;
        }
        window.addEventListener('mousedown', tmp_event);
        this.m_event = tmp_event;
    }

    setUp() {
        let tmp_event = () => {
            if (MouseEvent.new_object == null)
                return;
            MouseEvent.m_flag = 0;
            MouseEvent.c_flag = 0;
            // TODO: 편집창 추가
        }
        window.addEventListener('mouseup', tmp_event);
        this.m_event = tmp_event;
    }
}