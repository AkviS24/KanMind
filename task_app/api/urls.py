from django.urls import path

from .views import AssignedTasksView, TaskListView, ReviewingTasksView, TaskDetailView



urlpatterns=[
    path('tasks/', TaskListView.as_view(), name="task-list"),
    path('tasks/assigned-to-me/', AssignedTasksView.as_view(), name="assigned-tasks"),
    path('tasks/reviewing/', ReviewingTasksView.as_view(), name="reviewing-tasks"),
    path('tasks/<int:task_id>/', TaskDetailView.as_view(), name="task-detail"),
]