import json

from channels.generic.websocket import AsyncWebsocketConsumer
from . import ball

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connect")
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

b = ball.Ball()
p1 = ball.Stick((-15,0,0))
p2 = ball.Stick((15,0,0))
s1 = 0
s2 = 0

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        global b
        global p1
        global p2
        global s1
        global s2

        b.update(p1, p2, 2)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        ball_pos = b.pos
        paddle1_pos = p1.pos
        paddle2_pos = p2.pos
        score1 = s1
        score2 = s2

        # 클라이언트로부터 받은 메시지를 다시 클라이언트로 전송
        await self.send(text_data=json.dumps({
            'message': message,
            'ball_pos': ball_pos,
            'paddle1_pos': paddle1_pos,
            'paddle2_pos': paddle2_pos,
            'score1': score1,
            'score2': score2,
        }))