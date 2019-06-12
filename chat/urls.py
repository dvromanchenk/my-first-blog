
# from . import views
#
# urlpatterns = [
#     path('', views.index, name='index'),
# ]
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat_list', views.chat_list, name='chat_list'),
    path('<str:room_name>/', views.room, name='room'),
    path('disconnect/<str:room_name>/', views.disconnect, name='disconnect'),
]