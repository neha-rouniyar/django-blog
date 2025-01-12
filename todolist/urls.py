from django.contrib import admin
from django.urls import path,include

from todolist import views
from .views import TodoAPIView,TodoDetailAPIView

urlpatterns = [
    path('todo-get', views.getlist),
    path('apiview/get-todo-list/',TodoAPIView.as_view(),name='todolist'),
    path('apiview/get-todo-list/<int:pk>',TodoDetailAPIView.as_view(),name='todoDetailList')

]   
