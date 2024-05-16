class Ball {
    constructor() {
        this.pos = [0, 0, 0];
        this.dir = [-1, 0, 0];
    }

    len(vec) {
        return vec[0] * vec[0] + vec[1] * vec[1] + vec[2] * vec[2];
    }

    dist(vec1, vec2) {
        let answer = [];
        answer.push(vec1[0] - vec2[0]);
        answer.push(vec1[1] - vec2[1]);
        answer.push(vec1[2] - vec2[2]);
        return Math.sqrt(this.len(answer));
    }

    crash(posi) {
        let length = this.dist(this.pos, posi);
        if (length <= 0.5)
            return true;
        return false;
    }

    normalized(vec) {
        let answer = [vec[0], vec[1], vec[2]];
        let length = this.len(vec);
        if (Math.abs(length) < 0.000000001) {
            answer[0] = 0;
            answer[1] = 0;
            answer[2] = 0;
            return answer;
        }
        length = Math.sqrt(length);
        answer[0] /= length;
        answer[1] /= length;
        answer[2] /= length;
        return answer;
    }

    crashStick(stk) {
        if (this.pos[1] > stk.top[1] || this.pos[1] < stk.bottom[1])
            return false;
        if (Math.abs(this.pos[0] - stk.top[0]) > 0.5)
            return false;
        return true;
    }

    dot(vec1, vec2) {
        return Math.abs(vec1[0] * vec2[0] + vec1[1] * vec2[1] + vec1[2] * vec2[2]);
    }

    update(stick1, stick2, speed) {
        if (this.pos[0] > 15.5 || this.pos[0] < -15.5) {
            this.pos = [0, 0, 0];
            this.dir = [-1, 0, 0];
            return false;
        }
        let dir1 = [0, 0, 0], dir2 = [0, 0, 0], dir3 = [0, 0, 0], dir4 = [0, 0, 0];
        if (this.crash([this.pos[0], 7.75, 0])) {
            let dir_tmp = [0, -1, 0];
            let len = 2 * this.dot(dir_tmp, mulConst(-1, this.dir));
            dir_tmp = mulConst(len, dir_tmp);
            dir1 = this.normalized(sumDir(dir_tmp, this.dir));
        }
        if (this.crash([this.pos[0], -7.75, 0])) {
            let dir_tmp = [0, 1, 0];
            let len = 2 * this.dot(dir_tmp, mulConst(-1, this.dir));
            dir_tmp = mulConst(len, dir_tmp);
            dir2 = this.normalized(sumDir(dir_tmp, this.dir));
        }
        if (this.crashStick(stick1)) {
            let dir_tmp = [1, 0, 0];
            let len = 2 * this.dot(dir_tmp, mulConst(-1, this.dir));
            dir_tmp = mulConst(len, dir_tmp);
            dir3 = this.normalized(sumDir(dir_tmp, this.dir));
            dir3 = this.normalized(sumDir(dir3, stick1.dir));
        }
        if (this.crashStick(stick2)) {
            let dir_tmp = [-1, 0, 0];
            let len = 2 * this.dot(dir_tmp, mulConst(-1, this.dir));
            dir_tmp = mulConst(len, dir_tmp);
            dir4 = this.normalized(sumDir(dir_tmp, this.dir));
            dir4 = this.normalized(sumDir(dir4, stick2.dir));
        }
        let total = this.normalized(sumDir(dir1, dir2));
        total = this.normalized(sumDir(total, dir3));
        total = this.normalized(sumDir(total, dir4));
        if (isZero(total) == false)
            setSameDir(this.dir, total);
        let move = [this.dir[0], this.dir[1], this.dir[2]];
        move[0] *= speed;
        move[1] *= speed;
        move[2] *= speed;
        let after = sumDir(this.pos, move);
        let ddir = this.normalized(mulConst(2, subDir(after, this.pos)));
        let slope = (after[1] - this.pos[1]) / (after[0] - this.pos[0]);
        //test
        setZero(dir1);
        setZero(dir2);
        setZero(dir3);
        setZero(dir4);
        if (after[0] < -14.45 || after[0] > 14.45) {
            let x, y;
            if (after[0] < -14.25) {
                x = -14.25;
                y = slope * (x - this.pos[0]) + this.pos[1];
                if (y < stick1.top[1] + 0.5 && y > stick1.bottom[1] - 0.5) {
                    let d = mulConst(-0.5, ddir);
                    let tmp = [x, y, 0.0];
                    after = sumDir(tmp, d);
                    let dir_tmp = [1, 0, 0];
                    let len = 2 * this.dot(dir_tmp, mulConst(-1, this.dir));
                    dir_tmp = mulConst(len, dir_tmp);
                    dir3 = this.normalized(sumDir(dir_tmp, this.dir));
                    dir3 = this.normalized(sumDir(dir3, stick1.dir));
                }
            }
            else {
                x = 14.25;
                y = slope * (x - this.pos[0]) + this.pos[1];
                if (y < stick2.top[1] + 0.5 && y > stick1.bottom[1] - 0.5) {
                    let tmp = [x, y, 0.0];
                    let d = mulConst(-0.5, ddir);
                    after = sumDir(tmp, d);
                    let dir_tmp = [-1, 0, 0];
                    let len = 2 * this.dot(dir_tmp, mulConst(-1, this.dir));
                    dir_tmp = mulConst(len, dir_tmp);
                    dir4 = this.normalized(sumDir(dir_tmp, this.dir));
                    dir4 = this.normalized(sumDir(dir4, stick2.dir));
                }
            }
        }
        ddir = this.normalized(subDir(after, this.pos));
        slope = (after[1] - this.pos[1]) / (after[0] - this.pos[0]);
        if (after[1] > 7.45 || after[1] < -7.45) {
            if (after[0] > -14.75 && after[0] < 14.75) {
                let y, x;
                if (after[1] > 7.45) {
                    y = 7.25;
                    x = (y - this.pos[1]) / slope + this.pos[0];
                    let tmp = [x, y, 0.0];
                    let d = mulConst(-0.5, ddir);
                    after = sumDir(tmp, d);
                    let dir_tmp = [0, -1, 0];
                    let len = 2 * this.dot(dir_tmp, mulConst(-1, this.dir));
                    dir_tmp = mulConst(len, dir_tmp);
                    dir1 = this.normalized(sumDir(dir_tmp, this.dir));
                }
                else if (after[1] < -7.45) {
                    y = -7.25;
                    x = (y - this.pos[1]) / slope + this.pos[0];
                    let tmp = [x, y, 0.0];
                    let d = mulConst(-0.5, ddir);
                    after = sumDir(tmp ,d);
                    let dir_tmp = [0, 1, 0];
                    let len = 2 * this.dot(dir_tmp, mulConst(-1, this.dir));
                    dir_tmp = mulConst(len, dir_tmp);
                    dir2 = this.normalized(sumDir(dir_tmp, this.dir));
                }
            }
        }
        //test
        total = this.normalized(sumDir(dir1, dir2));
        total = this.normalized(sumDir(total, dir3));
        total = this.normalized(sumDir(total, dir4));
        if (isZero(total) == false)
            setSameDir(this.dir, total);
        // console.log("d3: ", dir3);
        // console.log(this.dir);
        // total = this.normalized(sumDir(dir3, dir4));
        this.pos = after;
        return true;
    }
}

function setZero(dir) {
    for (let i = 0; i < dir.length; i++)
        dir[i] = 0;
}

function isZero(dir) {
    for (let i = 0; i < 3; i++) {
        if (Math.abs(dir[i]) > 0.0000000001) 
            return false;
    }
    return true;
}

function isSame(dir1, dir2) {
    if (dir1.length != dir2.length)
        return false;
    for (let i = 0; i < dir1.length; i++) {
        if (dir1[i] != dir2[i])
            return false;
    }
    return true;
}

function setSameDir(des, src) {
    if (des.length != src.length)
        return false;
    for (let i = 0; i < des.length; i++)
        des[i] = src[i];
    return true;
}

function sumDir(dir1, dir2) {
    let answer = [0, 0, 0];
    answer[0] = dir1[0] + dir2[0];
    answer[1] = dir1[1] + dir2[1];
    answer[2] = dir1[2] + dir2[2];
    return answer;
}

function subDir(dir1, dir2) {
    let answer = [0.0, 0.0, 0.0];
    answer[0] = dir1[0] - dir2[0];
    answer[1] = dir1[1] - dir2[1];
    answer[2] = dir1[2] - dir2[2];
    return answer;
}

function mulConst(num, dir) {
    let answer = [0.0, 0.0, 0.0];
    answer[0] = num * dir[0];
    answer[1] = num * dir[1];
    answer[2] = num * dir[2];
    return answer;
}

class Stick {
    constructor(position) {
        this.top;
        this.bottom;
        this.pos = position;
        if (this.pos[0] < 0) {
            this.top = [this.pos[0] + 0.25, this.pos[1] + 1.5, 0];
            this.bottom = [this.pos[0] + 0.25, this.pos[1] - 1.5, 0];
        }
        else {
            this.top = [this.pos[0] - 0.25, this.pos[1] + 1.5, 0];
            this.bottom = [this.pos[0] - 0.25, this.pos[1] - 1.5, 0];
        }
        this.dir = [0, 0, 0];
    }
    update(move) {
        if (this.top[1] + move > 7.75 || this.bottom[1] + move < -7.75) {
            this.dir = [0, 0, 0];
            return;
        }
        this.top[1] += move;
        this.bottom[1] += move;
        this.pos[1] += move;
        if (move > 0)
            this.dir = [0, 1, 0];
        else if (move < 0)
            this.dir = [0, -1, 0];
        else
            this.dir = [0, 0, 0];
    }
}