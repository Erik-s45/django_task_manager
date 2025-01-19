from rest_framework import status
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Task
from .serializers import TaskSerializer, TaskDetailSerializer, RegisterSerializer
from .tasks import process_task


class RegisterView(CreateAPIView):
    """Вью для регистрации пользователей"""
    serializer_class = RegisterSerializer


class TaskPagination(PageNumberPagination):
    """Класс для создания пагинации задлач."""
    page_size = 5


class TaskView(ListCreateAPIView):
    """Вью для создания задачи и выведения списка задач.
    Содержит пагинацию и фильтрацию по статусу.
    Только для аутентифицированных пользователей по JWT токену."""
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    pagination_class = TaskPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def create(self, request, *args, **kwargs):
        # Проверка на допустимое количество задач
        max_task_amount = 5
        task_amount = Task.objects.filter(user=self.request.user, status__in=['scheduled', 'in_progress']).count()
        if task_amount >= max_task_amount:
            return Response(data={'message': 'Максимальное количество активных задач: 5.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Проверка полученных данных и сохранение задачи в базе
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(user=self.request.user)

        # Отправка задачи в Celery
        process_task.delay(task_id=task.id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user).order_by('-created_at')


class TaskDetailView(RetrieveAPIView):
    """Вью для просмотра отдельных задач.
    Только для аутентифицированных пользователей по JWT токену."""
    permission_classes = [IsAuthenticated]
    serializer_class = TaskDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)
