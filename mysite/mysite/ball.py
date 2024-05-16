import math

class Ball:
    def __init__(self):
        self.pos = [0, 0, 0]
        self.dir = [-1, 0, 0]

    def len(self, vec):
        return vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2

    def dist(self, vec1, vec2):
        answer = [
            vec1[0] - vec2[0],
            vec1[1] - vec2[1],
            vec1[2] - vec2[2]
        ]
        return math.sqrt(self.len(answer))

    def crash(self, posi):
        length = self.dist(self.pos, posi)
        return length <= 0.5

    def normalized(self, vec):
        answer = [vec[0], vec[1], vec[2]]
        length = self.len(vec)
        if abs(length) < 1e-9:
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

        dir1, dir2, dir3, dir4 = [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]

        if self.crash([self.pos[0], 7.75, 0]):
            dir_tmp = [0, -1, 0]
            len_tmp = 2 * self.dot(dir_tmp, mul_const(-1, self.dir))
            dir_tmp = mul_const(len_tmp, dir_tmp)
            dir1 = self.normalized(sum_dir(dir_tmp, self.dir))

        if self.crash([self.pos[0], -7.75, 0]):
            dir_tmp = [0, 1, 0]
            len_tmp = 2 * self.dot(dir_tmp, mul_const(-1, self.dir))
            dir_tmp = mul_const(len_tmp, dir_tmp)
            dir2 = self.normalized(sum_dir(dir_tmp, self.dir))

        if self.crash_stick(stick1):
            dir_tmp = [1, 0, 0]
            len_tmp = 2 * self.dot(dir_tmp, mul_const(-1, self.dir))
            dir_tmp = mul_const(len_tmp, dir_tmp)
            dir3 = self.normalized(sum_dir(dir_tmp, self.dir))
            dir3 = self.normalized(sum_dir(dir3, stick1.dir))

        if self.crash_stick(stick2):
            dir_tmp = [-1, 0, 0]
            len_tmp = 2 * self.dot(dir_tmp, mul_const(-1, self.dir))
            dir_tmp = mul_const(len_tmp, dir_tmp)
            dir4 = self.normalized(sum_dir(dir_tmp, self.dir))
            dir4 = self.normalized(sum_dir(dir4, stick2.dir))

        total = self.normalized(sum_dir(dir1, dir2))
        total = self.normalized(sum_dir(total, dir3))
        total = self.normalized(sum_dir(total, dir4))

        if not is_zero(total):
            set_same_dir(self.dir, total)

        move = [self.dir[0] * speed, self.dir[1] * speed, self.dir[2] * speed]
        after = sum_dir(self.pos, move)
        ddir = self.normalized(mul_const(2, sub_dir(after, self.pos)))
        if after[0] - self.pos[0]:
            slope = (after[1] - self.pos[1]) / (after[0] - self.pos[0])

        set_zero(dir1)
        set_zero(dir2)
        set_zero(dir3)
        set_zero(dir4)

        if after[0] < -14.45 or after[0] > 14.45:
            if after[0] < -14.25:
                x = -14.25
                y = slope * (x - self.pos[0]) + self.pos[1]
                if stick1.bottom[1] - 0.5 < y < stick1.top[1] + 0.5:
                    d = mul_const(-0.5, ddir)
                    after = sum_dir([x, y, 0.0], d)
                    dir_tmp = [1, 0, 0]
                    len_tmp = 2 * self.dot(dir_tmp, mul_const(-1, self.dir))
                    dir_tmp = mul_const(len_tmp, dir_tmp)
                    dir3 = self.normalized(sum_dir(dir_tmp, self.dir))
                    dir3 = self.normalized(sum_dir(dir3, stick1.dir))
            else:
                x = 14.25
                y = slope * (x - self.pos[0]) + self.pos[1]
                if stick2.bottom[1] - 0.5 < y < stick2.top[1] + 0.5:
                    after = sum_dir([x, y, 0.0], mul_const(-0.5, ddir))
                    dir_tmp = [-1, 0, 0]
                    len_tmp = 2 * self.dot(dir_tmp, mul_const(-1, self.dir))
                    dir_tmp = mul_const(len_tmp, dir_tmp)
                    dir4 = self.normalized(sum_dir(dir_tmp, self.dir))
                    dir4 = self.normalized(sum_dir(dir4, stick2.dir))

        ddir = self.normalized(sub_dir(after, self.pos))
        if after[0] - self.pos[0]:
            slope = (after[1] - self.pos[1]) / (after[0] - self.pos[0])

        if after[1] > 7.45 or after[1] < -7.45:
            if -14.75 < after[0] < 14.75:
                if after[1] > 7.45:
                    y = 7.25
                    x = (y - self.pos[1]) / slope + self.pos[0]
                    after = sum_dir([x, y, 0.0], mul_const(-0.5, ddir))
                    dir_tmp = [0, -1, 0]
                    len_tmp = 2 * self.dot(dir_tmp, mul_const(-1, self.dir))
                    dir_tmp = mul_const(len_tmp, dir_tmp)
                    dir1 = self.normalized(sum_dir(dir_tmp, self.dir))
                elif after[1] < -7.45:
                    y = -7.25
                    x = (y - self.pos[1]) / slope + self.pos[0]
                    after = sum_dir([x, y, 0.0], mul_const(-0.5, ddir))
                    dir_tmp = [0, 1, 0]
                    len_tmp = 2 * self.dot(dir_tmp, mul_const(-1, self.dir))
                    dir_tmp = mul_const(len_tmp, dir_tmp)
                    dir2 = self.normalized(sum_dir(dir_tmp, self.dir))

        total = self.normalized(sum_dir(dir1, dir2))
        total = self.normalized(sum_dir(total, dir3))
        total = self.normalized(sum_dir(total, dir4))

        if not is_zero(total):
            set_same_dir(self.dir, total)

        self.pos = after
        return True


def set_zero(dir):
    for i in range(len(dir)):
        dir[i] = 0

def is_zero(dir):
    return all(abs(d) < 1e-10 for d in dir)

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

def mul_const(num, dir):
    return [num * d for d in dir]


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

        if move > 0:
            self.dir = [0, 1, 0]
        elif move < 0:
            self.dir = [0, -1, 0]
        else:
            self.dir = [0, 0, 0]

