from django.urls import path, re_path, include
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
    path('thanks', views.thanks, name='thanks'),
    path('payment/success', views.payment_success, name='payment_success'),
    path('payment/error', views.payment_error, name='payment_error'),
    path('payment/cancel', views.payment_cancel, name='payment_cancel'),
    path('detail/<int:game_id>', views.game_detail, name='game_detail'),
    path('dev/inventory', views.inventory, name='inventory'),
    path('player/bought', views.player_game,name='player_game'),
    path('dev/inventory/<int:game_id>', views.show_modify_game, name='show_modify_game'),
    path('dev/inventory/<int:game_id>/update',views.modify_game, name='modify_game'),
    path('dev/inventory/<int:game_id>/delete',views.delete_game, name='delete_game'),
    path('dev/inventory/<int:game_id>/history',views.game_purchase_history, name='game_purchase_history'),
    path('auth/social/callback', views.choose_type, name='choose_type'),
    path('category/<str:category>', views.show_game_with_category,name="show_game_with_category"),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate_user_account, name='activate_user_account'),
]
