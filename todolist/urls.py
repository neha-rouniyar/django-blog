from django.contrib import admin
from django.urls import path,include
from .views import TodoViewSet
from rest_framework.routers import DefaultRouter
from todolist import views
from .views import TodoAPIView,TodoDetailAPIView,TodoListCreateGenericView,TodoRetrieveUpdateDestroyGenericAPIView,TodoMixinsView

router=DefaultRouter()
router.register('todos', TodoViewSet, basename='todo')



urlpatterns = [
    path('todo-get', views.getlist),
    
    # # urls using APIView
    path('apiview/get-todo-list/',TodoAPIView.as_view(),name='todolist'),
    path('apiview/get-todo-list/<int:pk>',TodoDetailAPIView.as_view(),name='todoDetailList'),

    # # urls using generics
    path('generic/get-todo-list/',TodoListCreateGenericView.as_view(),name='todolistcreategenericview'),
    path('generic/get-todo-list/<int:pk>',TodoRetrieveUpdateDestroyGenericAPIView.as_view(),name='todoRetrieveUpdateDestroyGenericView'),

     # # urls using mixins
    path('mixins/get-todo-list/',TodoMixinsView.as_view()),
    path('mixins/get-todo-list/<int:pk>',TodoMixinsView.as_view()),

    # # urls using ViewSet and Default Router
    path('viewset/',include(router.urls)),

]   
