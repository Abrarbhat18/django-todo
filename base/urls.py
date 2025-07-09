from django.urls import path
from .views import (
    TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete,
    CustomLoginView, RegisterPage, TaskReorder, ToggleCompleteView
)
from django.contrib.auth.views import LogoutView
from .views import ToggleCompleteView

urlpatterns = [
    # Auth
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('toggle/', ToggleCompleteView.as_view(), name='toggle-complete'),

    # Tasks
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),

    # ✅ AJAX toggle for complete/incomplete
    path('toggle/', ToggleCompleteView.as_view(), name='toggle-complete'),
]
