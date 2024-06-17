import { Setting } from "./graphics/Setting.js";
import { Ray } from "./graphics/Ray.js";
import { EventManager } from "./Event/EventManager.js";
// 추가 event dir, ray.js, pipeline,js, setting.js
// 수정 Mesh.js, box.js, sphere.js

class Main {
	static objects = [];
	static add_button;
	static cam = null;
	static ray = null;

	static entry() {
		Setting.setPipe();
		Main.objects = Setting.setBasicObjects();
		Main.add_button = Setting.setAddButton();
		Main.cam = Setting.setCam();
		Main.ray = new Ray(Main.cam);

		EventManager.setEventMouse(Main.ray, Main.add_button, Main.objects);

		requestAnimationFrame(Main.update);
	}

	static render() {
		Setting.setRender();
		Main.cam.putCam();
		let test = false;
		for (let i = 0; i < 5; i++)
			Main.objects[i].draw(false);
		for (let i = 5; i < Main.objects.length; i++) {
			let flag = false;
			for (let j = 1; j < i; j++) {
				if (Main.objects[i].collision(Main.objects[j]) === true) {
					flag = true;
					console.log("collision: ", i, ", ", j);
					test = true;
					break;
				}
			}
			Main.objects[i].draw(flag);
		}
		Main.add_button.draw(false);
		if (test)
			return false;
		return true; // test
	}

	static update() {
		let flag = Main.render();
		if (flag === false)
			return;
		requestAnimationFrame(Main.update);
	}
}
Main.entry();
