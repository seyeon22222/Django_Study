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

		EventManager.setEventKeyboard(Main.cam);
		EventManager.setEventMouse(Main.ray, Main.add_button, Main.objects);

		requestAnimationFrame(Main.update);
	}
	
	static render() {
		Setting.setRender();
		Main.cam.putCam();
		for (let i = 0; i < 6; i++) {
			if (i === 1)
				continue;
			Main.objects[i].draw(false);
		}
		for (let i = 6; i < Main.objects.length; i++) {
			let flag = false;
			if (Main.objects[i].pos[0] >= 14 || Main.objects[i].pos[0] <= -14)
				flag = true;
			if (Main.objects[i].pos[1] >= 7 || Main.objects[i].pos[1] <= -7)
				flag = true;
			let max_x = -100, max_y = -100, min_x = 100, min_y = 100;
			for (let k = 0; k < 4; k++) {
				if (Main.objects[i].colbox.vertices[k][0] > max_x)
					max_x = Main.objects[i].colbox.vertices[k][0];
				if (Main.objects[i].colbox.vertices[k][0] < min_x)
					min_x = Main.objects[i].colbox.vertices[k][0];
				if (Main.objects[i].colbox.vertices[k][1] > max_y)
					max_y = Main.objects[i].colbox.vertices[k][1];
				if (Main.objects[i].colbox.vertices[k][1] < min_y)
					min_y = Main.objects[i].colbox.vertices[k][1];
			}
			if (max_x > 14 || min_x < -14 || max_y > 7 || min_y < -7)
				flag = true;
			if (flag === false) {
				for (let j = 1; j < i; j++) {
					if (Main.objects[i].collision(Main.objects[j]) === true) {
						flag = true;
						break;
					}
				}
			}
			Main.objects[i].draw(flag);
		}
		Main.add_button.draw(false);
	}

	static update() {
		Main.render();
		requestAnimationFrame(Main.update);
	}
}
Main.entry();
