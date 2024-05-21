from django.urls import path
from . import views
from ft_user.views import UserViewSet


app_name = "ft_user"

urlpatterns = [
	path('', views.firstpage, name="firstpage"),
    path('login/', views.user_login, name="login"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path("logout/", views.logout_page, name = "logout"),
    path("login_suc/", views.login_suc, name = "success"),
    path("pong/", views.pong_with_com, name = "pong_with_computer"),
    path('api/User/', UserViewSet.as_view()),
    path('current_users_api/', views.current_users_api, name='current_users_api'),
    path('get_current_user_data/', views.get_current_user_data, name='current_user_data'),
    path('get_user_gamestat_details/', views.get_user_gamestat_detail, name='get_user_gamestat_details') #seycheon_0513
]
