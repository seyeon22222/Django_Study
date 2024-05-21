from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .utils import get_current_users
from django.http import JsonResponse
from django.contrib.auth.models import User

import json
from django.core.serializers.json import DjangoJSONEncoder #seycheon_0513 

from .serializers import (
    UserSerializer,
    UserDataSerializer,
)
from .models import MyUser
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from ft_user.models import MyUser
from ft_user.models import GameStat #seycheon_0513
from ft_user.models import MatchInfo #seycheon_0513
from ft_user.forms import signForm 
# Create your views here.

class UserViewSet(APIView):
    queryset = MyUser.objects.all()
    
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return Response(UserDataSerializer.data)
        else:
            return Response(UserSerializer.data)

    @action(detail=False, methods=["delete"])
    def delete_all(self, request):
        self.get_queryset().delete()
        return Response(status=204)

def firstpage(request):
	return render(request, "firstPage.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("인증 성공")
            login(request, user)
            return redirect("ft_user:success")
        else:
            # ToDo 중복 사용자 생성 시 에러 발생
            print("failed")
            return render(request, "login.html")
    else:
        return render(request, "login.html")

# ft_user:success  #seycheon_0513
def login_suc(request): 
    users = MyUser.objects.exclude(username='admin')
    users_json = json.dumps(list(users.values('username'))) 
    game_stat = GameStat.objects.exclude(user__username='admin')  
    
    # 사용자별 게임 스탯 정보 조회
    user_game_stats = []
    for user in users:
        game_stat = GameStat.objects.filter(user=user).values(
            'game_count', 'win_count', 'defeat_count', 'win_rate', 'reflect_rate'
        )
        user_game_stats.append({
            'username': user.username,
            'game_stats': list(game_stat)
        })
    # JSON으로 직렬화
    user_game_stats_json = json.dumps(user_game_stats, cls=DjangoJSONEncoder)
    return render(request, "success.html", {'users':users, 'users_json':users_json, 'game_stat':game_stat, 'game_stat_json':user_game_stats_json})  #seycheon_0513

def logout_page(request):
    logout(request)
    return redirect("ft_user:login")


def sign_up(request):
    if request.method == "POST":
        form = signForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = MyUser.objects.create_user(username, email=email, password=password)
            user.save()

            #seycheon_0513 회원가입시 gamestat 및 matchinfo 객체 생성
            game_stat = GameStat.objects.create(user=user)
            game_stat.save()

            match_info = MatchInfo.objects.create(user=user)
            match_info.save()

        return redirect("ft_user:firstpage")
    else:
        form = signForm()
        return render(request, "sign_up.html")
    

def pong_with_com(request):
    return render(request, "pong.html")


def current_users_api(request):
    current_users = get_current_users()
    usernames = [user.username for user in current_users]
    return JsonResponse({'current_users': usernames})


#seycheon_0513
def get_current_user_data(request): 
    # 현재 로그인한 사용자의 User 객체 가져오기
    current_user = request.user

    # 현재 로그인한 사용자의 game_status 가져오기
    try:
        game_stat = GameStat.objects.get(user__username=current_user)
        game_stat_data = {
            'game_count': game_stat.game_count,
            'win_count': game_stat.win_count,
            'defeat_count': game_stat.defeat_count,
            'win_rate': game_stat.win_rate,
            'reflect_rate': game_stat.reflect_rate
        }
    except GameStat.DoesNotExist:
        game_stat_data = {
            'game_count': -1,
            'win_count': -1,
            'defeat_count': -1,
            'win_rate': -1,
            'reflect_rate': -1
        }

    # 현재 로그인한 사용자의 데이터를 JSON 형식으로 묶기
    user_data = {
        'user_id' : current_user.user_id,
        'username': current_user.username,
        'email': current_user.email,
        'game_stat': game_stat_data
    }
    # JSON 응답 생성
    return JsonResponse(user_data)

#seycheon_0513
def get_user_gamestat_detail(request):
    if request.method == "GET":
        username = request.GET.get('username')  # 요청에서 사용자 이름 가져오기
        try:
            user = MyUser.objects.get(username=username)  # 사용자 객체 가져오기
        except MyUser.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)

        # 사용자의 게임 스탯 정보 가져오기
        try:
            game_stat = GameStat.objects.get(user=user)
            game_stat_detail = {
                'game_count': game_stat.game_count,
                'win_count': game_stat.win_count,
                'defeat_count': game_stat.defeat_count,
                'win_rate': game_stat.win_rate,
                'reflect_rate': game_stat.reflect_rate
            }
        except GameStat.DoesNotExist:
            game_stat_detail = None

        # 사용자의 최근 10개의 매치 정보 가져오기
        recent_matches = MatchInfo.objects.filter(user=user).order_by('-match_date')[:10]
        recent_matches_detail = []
        for match in recent_matches:
            match_detail = {
                'match_date': match.match_date,
                'match_result': match.match_result
            }
            recent_matches_detail.append(match_detail)

        # JSON 형식으로 응답 반환
        return JsonResponse({
            'username': username,
            'game_stat': game_stat_detail,
            'recent_matches': recent_matches_detail
        })

    else:
        return JsonResponse({'error': 'GET method is required'}, status=400)


#seychon_0513 game_end시 데이터베이스 업데이트 예시
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from .models import MatchInfo,GameStat, MyUser

# @csrf_exempt
# def update_game_stats(request):
#     if request.method == "POST":
#         # POST 요청의 body에서 데이터 추출
#         data = json.loads(request.body)
#         player_stats = data.get('playerStats', [])  # 각 플레이어별 게임 스탯 정보

#         # 게임 스탯 업데이트 로직
#         for player_stat in player_stats:
#             player = player_stat.get('player')
#             winner = player_stat.get('winner')
#             game_date = player_stat.get('gameDate')
#             ball_thrown_count = player_stat.get('ballThrownCount', 0)
#             ball_hit_count = player_stat.get('ballHitCount', 0)

#             # 각 플레이어의 스탯을 업데이트
#             game_stat, _ = GameStat.objects.get_or_create(user=player)
#             game_stat.game_count += 1
#             if winner:
#                 game_stat.win_count += 1
#             else:
#                 game_stat.defeat_count += 1
#             # 공이 날아온 횟수와 받아친 횟수를 이용하여 reflect_rate 업데이트
#             if ball_thrown_count > 0:
#                 reflect_rate = ball_hit_count / ball_thrown_count
#             else:
#                 reflect_rate = 0
#             game_stat.reflect_rate += reflect_rate
#             game_stat.save()

#         # 응답 생성
#         return JsonResponse({'message': '게임 스탯이 업데이트되었습니다.'})

#     else:
#         return JsonResponse({'error': 'POST 메소드만 허용됩니다.'})
