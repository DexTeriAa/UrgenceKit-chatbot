from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('home/', views.home, name="home"),
    path('chat/', views.generate_chat, name='generate_chat'),
    path('map/', views.map_view, name='map_view'),   
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name='logout'),
    path('register_user', views.register_user, name='register_user')
]