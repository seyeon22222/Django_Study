from django.urls import path
from . import views

app_name = "chatting"

urlpatterns = [
	path('Rooms/', views.rooms, name = 'rooms'),
    path('room_make/', views.room_make, name='room_make'),
    path('room_make_or_get/', views.room_make_or_get, name='room_make_or_get'),
    path('<slug:slug>/', views.room, name='room'),
]

