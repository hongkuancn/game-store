from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup_page, name="signup"),
    path('login', views.login_page, name="login"),
    path('signup_user', views.signup_user, name='signup_user'),
    path('log_user_in', views.log_user_in, name='log_user_in'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('newgame_page', views.newgame_page, name='newgame_page'),
    path('create_new_game', views.create_new_game, name='create_new_game'),
    path('gaming/ajax', views.gaming, name='gameing'),
    path('gaming/<int:game_id>/', views.games, name='games'),
    path('thanks', views.thanks, name='thanks'),
]
