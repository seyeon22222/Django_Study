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
b = ball.Ball()
p1 = ball.Stick([-15,0,0])
p2 = ball.Stick([15,0,0])
class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.loop = asyncio.get_event_loop()
        self.task = self.loop.create_task(self.send_message())
        global players
        global b
        global p1
        global p2
        
        ball_pos = b.pos
        paddle1_pos = p1.pos
        paddle2_pos = p2.pos
        players += 1
        players %= 3
        if players == 0:
            players = 1
        await self.send(text_data=json.dumps({
            "players": players,
            'ball_pos': ball_pos,
            'paddle1_pos': paddle1_pos,
            'paddle2_pos': paddle2_pos,
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
        while True:
            dt = (time.perf_counter() - lastTime)
            lastTime = time.perf_counter()

            p1.update(p1.dir[1] * 10 * dt)
            p2.update(p2.dir[1] * 10 * dt)
            b.update(p1, p2, dt * 20)
            
            ball_pos = b.pos
            paddle1_pos = p1.pos
            paddle2_pos = p2.pos
            score1 = b.point1
            score2 = b.point2
            # 클라이언트로 메시지 보내기
            await self.send(json.dumps({
            'ball_pos': ball_pos,
            'paddle1_pos': paddle1_pos,
            'paddle2_pos': paddle2_pos,
            'score1': score1,
            'score2': score2,
            }))
            # 초 대기
            await asyncio.sleep(0.001)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        player = text_data_json['players']

        if player is not None:
            player = int(player)
        if (message == '1pup' and player % 2 == 1):
            p1.dir[1] = 1
        if (message == '1pdown' and player % 2 == 1):
            p1.dir[1] = -1
        if (message == '2pup' and player % 2 == 0):
            p2.dir[1] = 1
        if (message == '2pdown' and player % 2 == 0):
            p2.dir[1] = -1
        if (message == '1pupstop' and p1.dir[1] == 1 and player % 2 == 1):
            p1.dir[1] = 0
        if (message == '1pdownstop' and p1.dir[1] == -1 and player % 2 == 1):
            p1.dir[1] = 0
        if (message == '2pupstop' and p2.dir[1] == 1 and player % 2 == 0):
            p2.dir[1] = 0
        if (message == '2pdownstop' and p2.dir[1] == -1 and player % 2 == 0):
            p2.dir[1] = 0