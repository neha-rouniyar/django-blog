from django.urls import path, include
from . import views

urlpatterns=[
    path('hello',views.homapage),

    # urls for insert
    path('task/form',views.task_form),
    path('task/add',views.insert_task, name='add_task'),
    path('view/task',views.view_tasks, name='view_task'),
    path('edit/task/<int:task_id>/',views.edit_task, name='edit_task'),
    path('update/task/<int:task_id>/',views.update_task, name='update_task'),
    path('delete/task/<int:task_id>/',views.delete_task, name='delete_task'),





]