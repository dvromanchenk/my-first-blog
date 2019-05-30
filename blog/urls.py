from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('goto_login', views.goto_login, name='goto_login'),
]