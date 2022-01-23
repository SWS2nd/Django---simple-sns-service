from django.urls import path
from . import views # 현재 app 내 views.py를 불러오기.

urlpatterns = [
    path('sign-up/', views.sign_up_view, name='sign-up'),
    path('sign-in/', views.sign_in_view, name='sign-in'),
    path('logout/', views.logout, name='logout'),
    path('user/', views.user_view, name='user-list'),
    # 여기의 id는 해당하는 유저의 id
    path('user/follow/<int:id>/', views.user_follow, name='user-follow'),
]