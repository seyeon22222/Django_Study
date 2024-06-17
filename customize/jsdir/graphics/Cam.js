import { Mat4x4} from "./Mat4x4.js";

export class Cam {
    constructor(gl) {
        this.cam_mat = Mat4x4.identityMat();
        this.view_mat = Mat4x4.identityMat();
        this.proj_mat = Mat4x4.identityMat();
        this.near;
        this.pos = [0, 0, 0, 1];
        this.gl = gl;
        this.vp_loc;
    }

    setCamMat(look, up, pos) {
        for (let i = 0; i < 3; i++)
            this.pos[i] = pos[i];
        this.cam_mat = Mat4x4.camMatrix(look, up, pos);
        this.view_mat = Mat4x4.viewMatrix(this.cam_mat);
    }

    rotCam(degree) {
        let rot = Mat4x4.rotMatAxisZ(degree);
        this.cam_mat = Mat4x4.multipleMat4(rot, this.cam_mat);
        this.view_mat = Mat4x4.viewMatrix(this.cam_mat);
    }

    moveCam(pos) {
        this.pos = pos;
        let move_mat = Mat4x4.transportMat([pos[0], pos[1], pos[2], 1]);
        this.cam_mat = Mat4x4.multipleMat4(move_mat, this.cam_mat);
        this.view_mat = Mat4x4.viewMatrix(this.cam_mat);
    }

    projMat(fov_rad, width, height, near, far) {
        this.near = near;
        this.proj_mat = Mat4x4.projectionMatrix(
            fov_rad,
            near,
            far,
            width / height
        );
    }

    setViewProjLoc(loc) {
        this.vp_loc = loc;
    }

    putCam() {
        let vp_mat = Mat4x4.multipleMat4(this.proj_mat, this.view_mat);
        this.gl.uniformMatrix4fv(this.vp_loc, true, vp_mat);
    }
}