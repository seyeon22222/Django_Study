import math

MIN = 1e-9

class Ball:
    def __init__(self):
        self.pos = [0, 0, 0]
        self.dir = [-1, 0, 0]

    def len(self, vec):
        return vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2

    def dist(self, vec1, vec2):
        answer = [vec1[i] - vec2[i] for i in range(3)]
        return math.sqrt(self.len(answer))

    def crash(self, posi):
        length = self.dist(self.pos, posi)
        return length <= 0.5

    def normalized(self, vec):
        answer = vec[:]
        length = self.len(vec)
        if math.isclose(length, 0, abs_tol=1e-9):
            return [0, 0, 0]
        length = math.sqrt(length)
        return [v / length for v in answer]

    def crashStick(self, stk):
        if self.pos[1] > stk.top[1] or self.pos[1] < stk.bottom[1]:
            return False
        return abs(self.pos[0] - stk.top[0]) <= 0.5

    def dot(self, vec1, vec2):
        return abs(sum(vec1[i] * vec2[i] for i in range(3)))

    def update(self, stick1, stick2, speed):
        if self.pos[0] > 15.5 or self.pos[0] < -15.5:
            self.pos = [0, 0, 0]
            self.dir = [-1, 0, 0]
            return False
        
        dir_norm = [0, 0, 0]
        if self.crash([self.pos[0], 7.75, 0]):
            dir_norm = sum_dir(dir_norm, [0, -1, 0])
        if self.crash([self.pos[0], -7.75, 0]):
            dir_norm = sum_dir(dir_norm, [0, 1, 0])
        if self.crashStick(stick1):
            dir_norm = sum_dir(dir_norm, [1, 0, 0])
            dir_norm = sum_dir(dir_norm, stick1.dir)
        if self.crashStick(stick2):
            dir_norm = sum_dir(dir_norm, [-1, 0, 0])
            dir_norm = sum_dir(dir_norm, stick2.dir)
        
        dir_norm = self.normalized(dir_norm)
        len_ = self.dot(dir_norm, mul_const(-1, self.dir))
        s_norm = mul_const(2 * len_, dir_norm)
        dir_norm = sum_dir(self.dir, s_norm)
        
        len_ = abs(dir_norm[0])
        if len_ < MIN:
            dir_norm[0] = -1 if self.dir[0] > 0 else 1
            len_ = 1
        
        dir_norm = mul_const(1.0 / len_, dir_norm)
        move = mul_const(speed, dir_norm)
        after = sum_dir(self.pos, move)
        
        ddir = self.normalized(mul_const(2, sub_dir(after, self.pos)))
        slope = (after[1] - self.pos[1]) / (after[0] - self.pos[0])
        flag = 0
        dir_norm2 = [0, 0, 0]
        
        if after[0] < -14.45 or after[0] > 14.45:
            if after[0] < -14.25:
                x = -14.25
                y = slope * (x - self.pos[0]) + self.pos[1]
                if stick1.bottom[1] - 0.5 < y < stick1.top[1] + 0.5:
                    after = sum_dir([x, y, 0.0], mul_const(-0.5, ddir))
                    flag = 1
                    dir_norm2 = sum_dir(dir_norm2, [1, 0, 0])
                    dir_norm2 = sum_dir(dir_norm2, stick1.dir)
            else:
                x = 14.25
                y = slope * (x - self.pos[0]) + self.pos[1]
                if stick2.bottom[1] - 0.5 < y < stick2.top[1] + 0.5:
                    after = sum_dir([x, y, 0.0], mul_const(-0.5, ddir))
                    flag = 1
                    dir_norm2 = sum_dir(dir_norm2, [-1, 0, 0])
                    dir_norm2 = sum_dir(dir_norm2, stick2.dir)
        
        ddir = self.normalized(sub_dir(after, self.pos))
        slope = (after[1] - self.pos[1]) / (after[0] - self.pos[0])
        if after[1] > 7.45 or after[1] < -7.45:
            if -14.75 < after[0] < 14.75:
                if after[1] > 7.45:
                    y = 7.25
                    x = (y - self.pos[1]) / slope + self.pos[0]
                    after = sum_dir([x, y, 0.0], mul_const(-0.5, ddir))
                    flag = 1
                    dir_norm2 = sum_dir(dir_norm2, [0, -1, 0])
                elif after[1] < -7.45:
                    y = -7.25
                    x = (y - self.pos[1]) / slope + self.pos[0]
                    after = sum_dir([x, y, 0.0], mul_const(-0.5, ddir))
                    flag = 1
                    dir_norm2 = sum_dir(dir_norm2, [0, 1, 0])
        
        if flag:
            dir_norm2 = self.normalized(dir_norm2)
            len_ = abs(dir_norm2[0])
            if len_ < MIN:
                dir_norm2[0] = -1 if self.dir[0] < 0 else 1
                len_ = 1
            dir_norm2 = mul_const(1.0 / len_, dir_norm2)
            set_same_dir(self.dir, dir_norm2)
        else:
            set_same_dir(self.dir, dir_norm)
        set_same_dir(self.pos, after)
        return True


def set_zero(dir_):
    for i in range(len(dir_)):
        dir_[i] = 0

def is_zero(dir_):
    return all(math.isclose(dir_[i], 0, abs_tol=1e-10) for i in range(3))

def is_same(dir1, dir2):
    return dir1 == dir2

def set_same_dir(des, src):
    if len(des) != len(src):
        return False
    for i in range(len(des)):
        des[i] = src[i]
    return True

def sum_dir(dir1, dir2):
    return [dir1[i] + dir2[i] for i in range(3)]

def sub_dir(dir1, dir2):
    return [dir1[i] - dir2[i] for i in range(3)]

def mul_const(num, dir_):
    return [num * dir_[i] for i in range(3)]


class Stick:
    def __init__(self, position):
        self.pos = position
        self.top = position
        self.bottom = position
        if self.pos[0] < 0:
            self.top = [self.pos[0] + 0.25, self.pos[1] + 1.5, 0]
            self.bottom = [self.pos[0] + 0.25, self.pos[1] - 1.5, 0]
        else:
            self.top = [self.pos[0] - 0.25, self.pos[1] + 1.5, 0]
            self.bottom = [self.pos[0] - 0.25, self.pos[1] - 1.5, 0]
        self.dir = [0, 0, 0]

    def update(self, move):
        if self.top[1] + move > 7.75 or self.bottom[1] + move < -7.75:
            self.dir = [0, 0, 0]
            return
        self.top[1] += move
        self.bottom[1] += move
        self.pos[1] += move
        if move > 0:
            self.dir = [0, 1, 0]
        elif move < 0:
            self.dir = [0, -1, 0]
        else:
            self.dir = [0, 0, 0]
