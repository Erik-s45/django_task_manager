from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import RegisterView, TaskView, TaskDetailView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('tasks/', TaskView.as_view()),
    path('tasks/<int:pk>/', TaskDetailView.as_view()),
]
