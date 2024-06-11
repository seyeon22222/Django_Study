import json
import asyncio
import time

from channels.generic.websocket import AsyncWebsocketConsumer
from . import ball

s1 = 0
s2 = 0
dt = 0
lastTime = 0
players = 0
b = ball.Ball(0.5)
p1 = ball.Stick([-15,1.5,0], 0.5, 3)
p2 = ball.Stick([-15,-1.5,0], 0.5, 3)
p3 = ball.Stick([15, 1.5,0], 0.5, 3)
p4 = ball.Stick([15, -1.5, 0], 0.5, 3)
paddles = []
paddles.append(p1)
paddles.append(p2)
paddles.append(p3)
paddles.append(p4)
obtacles = []
obtacles.append(ball.Box(30, 0.5))
obtacles[0].movePos([0, 8, 0])
obtacles.append(ball.Box(30, 0.5))
obtacles[1].movePos([0, -8, 0])
obtacles[1].rotBox(0)

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.loop = asyncio.get_event_loop()
        self.task = self.loop.create_task(self.send_message())
        global players
        global b
        global p1
        global p2
        global p3
        global p4
        global paddles
        global obtacles
        global s1
        global s2
        
        ball_pos = b.pos
        paddle1_pos = p1.pos
        paddle2_pos = p2.pos
        paddle3_pos = p3.pos
        paddle4_pos = p4.pos
        players += 1
        players %= 3
        if players == 0:
            players = 1
        await self.send(text_data=json.dumps({
            "players": players,
            'ball_pos': ball_pos,
            'paddle1_pos': paddle1_pos,
            'paddle2_pos': paddle2_pos,
            'paddle3_pos': paddle3_pos,
            'paddle4_pos': paddle4_pos,
            'score1': s1,
            'score2': s2
            }))

    async def disconnect(self, close_code):
        self.task.cancel()

    async def send_message(self):
        global s1
        global s2
        global dt
        global lastTime
        global b
        global p1
        global p2
        global p3
        global p4
        global paddles
        global obtacles
        global players
        while True:
            dt = (time.perf_counter() - lastTime)
            lastTime = time.perf_counter()

            map_length = obtacles[0].bot1[1] - obtacles[1].top1[1]
            p1.update(p1.dir[1] * 10 * dt, obtacles[0].bot1[1], obtacles[1].top1[1] + map_length / 2)
            p2.update(p2.dir[1] * 10 * dt, obtacles[0].bot1[1], obtacles[1].top1[1] + map_length / 2)
            p3.update(p3.dir[1] * 10 * dt, obtacles[0].bot1[1] - map_length / 2, obtacles[1].top1[1])
            p4.update(p4.dir[1] * 10 * dt, obtacles[0].bot1[1] - map_length / 2, obtacles[1].top1[1])
            b.pos[2] = 1
            flag = b.update(paddles, obtacles, dt * 20)
            b.pos[2] = 0
            
            ball_pos = b.pos
            paddle1_pos = p1.pos
            paddle2_pos = p2.pos
            paddle3_pos = p3.pos
            paddle4_pos = p4.pos
            score1 = b.point1
            score2 = b.point2
            # 클라이언트로 메시지 보내기
            await self.send(json.dumps({
            'ball_pos': ball_pos,
            'paddle1_pos': paddle1_pos,
            'paddle2_pos': paddle2_pos,
            'paddle3_pos': paddle3_pos,
            'paddle4_pos': paddle4_pos,
            'score1': score1,
            'score2': score2,
            'players': players
            }))
            # 초 대기
            await asyncio.sleep(0.001)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        player = text_data_json['players']

        if player is not None:
            player = int(player)
        if (message == 'up' and player % 2 == 1):
            p1.dir[1] = 1
        if (message == 'down' and player % 2 == 1):
            p1.dir[1] = -1
        if (message == 'up' and player % 2 == 0):
            p2.dir[1] = 1
        if (message == 'down' and player % 2 == 0):
            p2.dir[1] = -1
        if (message == 'upstop' and p1.dir[1] == 1 and player % 2 == 1):
            p1.dir[1] = 0
        if (message == 'downstop' and p1.dir[1] == -1 and player % 2 == 1):
            p1.dir[1] = 0
        if (message == 'upstop' and p2.dir[1] == 1 and player % 2 == 0):
            p2.dir[1] = 0
        if (message == 'downstop' and p2.dir[1] == -1 and player % 2 == 0):
            p2.dir[1] = 0