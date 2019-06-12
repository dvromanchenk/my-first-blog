from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('new_user', views.new_user_view, name='new_user'),
    path('personal_cabinet', views.personal_cabinet, name='personal_cabinet'),
    path('my_posts', views.my_posts, name='my_posts'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('post/mark/<int:pk>', views.mark_to_post, name='mark_to_post'),
    path('register/confirm/<str:key>/', views.confirm_account, name='confirm_account'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('user_list', views.user_list, name='user_list'),
    path('user_list/<int:pk>', views.user_detail, name='user_detail'),
]
