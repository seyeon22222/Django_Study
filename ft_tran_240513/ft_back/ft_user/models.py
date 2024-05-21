from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import datetime

# 유저 정보
class MyUser(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(unique=True)
    def __str__(self):
        return str(self.username)
    
    # imageURL = models.URLField(blank=True, null=True)
    

# 게임 스탯
class GameStat(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='game_stat')
    game_count = models.IntegerField(default=0)
    win_count = models.IntegerField(default=0) 
    defeat_count = models.IntegerField(default=0)
    win_rate = models.IntegerField(default=0)
    reflect_rate = models.IntegerField(default=0) 

#seycheon_0513 매치 정보 사용자와 개별 매치 정보 간에는 일대다(One-to-Many) 관계
class MatchInfo(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='match_info')
    match_date = models.DateTimeField(default=datetime.now())
    match_result = models.CharField(default='', max_length=1) 
    

#전체 회원의 매치 정보를 저장하기 위한 모델
# class MatchGroup(models.Model):
#     matches = models.ManyToManyField(MatchInfo, related_name='match_group')
#     group_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Match Group on {self.group_date}"