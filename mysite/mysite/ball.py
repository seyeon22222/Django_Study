import math

MIN = 0.000000001

def set_same_dir(des, src):
    if len(des) != len(src):
        return False
    for i in range(len(des)):
        des[i] = src[i]
    return True

def sum_dir(dir1, dir2):
    return [dir1[0] + dir2[0], dir1[1] + dir2[1], dir1[2] + dir2[2]]

def sub_dir(dir1, dir2):
    return [dir1[0] - dir2[0], dir1[1] - dir2[1], dir1[2] - dir2[2]]

def mul_const(num, dir):
    return [num * dir[0], num * dir[1], num * dir[2]]

def set_zero(dir):
    for i in range(len(dir)):
        dir[i] = 0

def is_zero(dir):
    return all(abs(d) < 1e-10 for d in dir)

def is_same(dir1, dir2):
    if len(dir1) != len(dir2):
        return False
    return all(dir1[i] == dir2[i] for i in range(len(dir1)))

class Ball:
    def __init__(self):
        self.pos = [0, 0, 0]
        self.dir = [1, 0, 0]

    def len(self, vec):
        return vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2

    def dist(self, vec1, vec2):
        answer = [vec1[0] - vec2[0], vec1[1] - vec2[1], vec1[2] - vec2[2]]
        return math.sqrt(self.len(answer))

    def crash(self, posi):
        length = self.dist(self.pos, posi)
        return length <= 0.5

    def normalized(self, vec):
        length = self.len(vec)
        if abs(length) < MIN:
            return [0, 0, 0]
        length = math.sqrt(length)
        return [v / length for v in vec]

    def crash_stick(self, stk):
        if self.pos[1] > stk.top[1] or self.pos[1] < stk.bottom[1]:
            return False
        if abs(self.pos[0] - stk.top[0]) > 0.5:
            return False
        return True

    def dot(self, vec1, vec2):
        return abs(vec1[0] * vec2[0] + vec1[1] * vec2[1] + vec1[2] * vec2[2])

    def update(self, stick1, stick2, speed):
        if self.pos[0] > 15.5 or self.pos[0] < -15.5:
            self.pos = [0, 0, 0]
            self.dir = [-1, 0, 0]
            return False

        stick1_flag = False
        stick2_flag = False
        dir_norm = [0, 0, 0]

        if self.crash([self.pos[0], 7.75, 0]):
            dir_norm = sum_dir(dir_norm, [0, -1, 0])
        if self.crash([self.pos[0], -7.75, 0]):
            dir_norm = sum_dir(dir_norm, [0, 1, 0])
        if self.crash_stick(stick1):
            dir_norm = sum_dir(dir_norm, [1, 0, 0])
            dir_norm = sum_dir(dir_norm, stick1.dir)
            stick1_flag = True
        if self.crash_stick(stick2):
            dir_norm = sum_dir(dir_norm, [-1, 0, 0])
            dir_norm = sum_dir(dir_norm, stick2.dir)
            stick2_flag = True

        dir_norm = self.normalized(dir_norm)
        length = self.dot(dir_norm, mul_const(-1, self.dir))
        s_norm = mul_const(2 * length, dir_norm)
        dir_norm = sum_dir(self.dir, s_norm)

        length = abs(dir_norm[0])
        if length < MIN:
            if self.dir[0] > 0:
                dir_norm[0] = -1 if stick2_flag else 1
            else:
                dir_norm[0] = 1 if stick1_flag else -1
            length = 1
        dir_norm = mul_const(1.0 / length, dir_norm)
        move = mul_const(speed, dir_norm)
        after = sum_dir(self.pos, move)

        set_same_dir(self.pos, after)
        set_same_dir(self.dir, self.normalized(dir_norm))
        return True

class Stick:
    def __init__(self, position):
        self.pos = position
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
        self.dir = [0, 1, 0] if move > 0 else [0, -1, 0] if move < 0 else [0, 0, 0]
