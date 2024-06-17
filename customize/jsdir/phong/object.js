import { Mat4x4} from "../graphics/Mat4x4.js";

const MIN = 0.00000000001

function subDir(dir1, dir2) {
    let ans = [];
    for (let i = 0; i < dir1.length; i++)
        ans.push(dir1[i] - dir2[i])
    return ans;
}

function dotDir(src, des) {
    let ans = 0;
    for (let i = 0; i < 3; i++)
        ans += src[i] * des[i];
    return ans;
}

function getLength(src) {
    let len = src[0] * src[0] + src[1] * src[1] + src[2] * src[2];
    len = Math.sqrt(len);
    return len;
}

function crossProduct(vec1, vec2) {
	let res = [0, 0, 0];
	res[0] = vec1[1] * vec2[2] - vec1[2] * vec2[1];
	res[1] = vec1[2] * vec2[0] - vec1[0] * vec2[2];
	res[2] = vec1[0] * vec2[1] - vec1[1] * vec2[0];
    res[3] = 0;
	return res;
}

function normalizeVec(vec) {
	let length = Math.sqrt(vec[0] * vec[0] + vec[1] * vec[1] + vec[2] * vec[2]);
	let res = new Array(3);
	res[0] = vec[0] / length;
	res[1] = vec[1] / length;
	res[2] = vec[2] / length;
    res[3] = vec[3]
	return res;
}

export class CollisionBox {
    constructor(width, height, depth) {
        this.pos = [0, 0, 0, 1]
        this.degree = 0
        this.width = width
        this.height = height
        this.depth = depth
        this.up = [0, 1, 0, 0];
        this.right = [1, 0, 0, 0];
        this.forward = [0, 0, 1, 0];
        this.upPoint = [0, height / 2, 0, 1];
        this.foPoint = [0, 0, depth / 2, 1];
        this.riPoint = [width / 2, 0, 0, 1];
    }

    rotBox(degree) {
        let rotMat = Mat4x4.rotMatAxisZ(degree);
        this.up = Mat4x4.multipleMat4AndVec4(rotMat, this.up);
        this.right = Mat4x4.multipleMat4AndVec4(rotMat, this.right);
        this.forward = Mat4x4.multipleMat4AndVec4(rotMat, this.forward);
        this.upPoint = Mat4x4.multipleMat4AndVec4(rotMat, this.upPoint);
        this.foPoint = Mat4x4.multipleMat4AndVec4(rotMat, this.foPoint);
        this.riPoint = Mat4x4.multipleMat4AndVec4(rotMat, this.riPoint);
        
        this.upPoint = subDir(this.upPoint, this.pos);
        this.upPoint[3] = 1;
        this.foPoint = subDir(this.foPoint, this.pos);
        this.foPoint[3] = 1;
        this.riPoint = subDir(this.riPoint, this.pos);
        this.riPoint[3] = 1;
    }

    moveBox(mvX, mvY, mvZ) {
        let movMat = Mat4x4.transportMat([mvX, mvY, mvZ, 1])
        this.pos = Mat4x4.multipleMat4AndVec4(movMat, this.pos)
        this.upPoint = Mat4x4.multipleMat4AndVec4(movMat, this.upPoint);
        this.foPoint = Mat4x4.multipleMat4AndVec4(movMat, this.foPoint);
        this.riPoint = Mat4x4.multipleMat4AndVec4(movMat, this.riPoint);

        this.upPoint = subDir(this.upPoint, this.pos);
        this.upPoint[3] = 1;
        this.foPoint = subDir(this.foPoint, this.pos);
        this.foPoint[3] = 1;
        this.riPoint = subDir(this.riPoint, this.pos);
        this.riPoint[3] = 1;
    }

    collision(otherBox) {
        //TODO 수정 필요
        let ab = subDir(this.pos, otherBox.pos);
        let unique = [this.upPoint, this.riPoint, this.foPoint, otherBox.upPoint, otherBox.riPoint, otherBox.foPoint];
        let SAT = [this.up, this.right, this.forward, otherBox.up, otherBox.right, otherBox.forward];
        SAT.push(crossProduct(this.up, otherBox.up));
        SAT.push(crossProduct(this.up, otherBox.right));
        SAT.push(crossProduct(this.up, otherBox.forward));
        SAT.push(crossProduct(this.right, otherBox.up));
        SAT.push(crossProduct(this.right, otherBox.right));
        SAT.push(crossProduct(this.right, otherBox.forward));
        SAT.push(crossProduct(this.forward, otherBox.up));
        SAT.push(crossProduct(this.forward, otherBox.right));
        SAT.push(crossProduct(this.forward, otherBox.forward));
        console.log("collision start !!!");
        console.log("SAT: ", SAT);
        console.log("unique: ", unique);
        console.log("this pos: ", this.pos, ", oth box pos: ", otherBox.pos);
        for (let i = 0; i < SAT.length; i++) {
            let total = 0;
            if (getLength(SAT[i]) < MIN)
                continue;
            SAT[i] = normalizeVec(SAT[i]);
            for (let j = 0; j < 6; j++) {
                console.log("dot SAT ", i , " and unique ", j, " : ", dotDir(SAT[i], unique[j]));
                console.log("unique ", j, " : ", unique[j]);
                total += Math.abs(dotDir(SAT[i], unique[j]));
            }
            let dist = Math.abs(dotDir(ab, SAT[i]));
            console.log("SAT ", i, " : ", SAT[i]);
            console.log("ab: ", ab);
            console.log("dist: ", dist, ", total: ", total);
            if (dist >= total) {
                console.log("collision detect\n\n");
                return false;
            }
            console.log("\n\n");
        }
        return true;
    }
};