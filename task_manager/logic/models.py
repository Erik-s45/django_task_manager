from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """Модель задачи."""
    STATUS_CHOICES = [
        ('scheduled', 'Запланировано'),
        ('in_progress', 'Выполняется'),
        ('completed', 'Выполнено'),
        ('error', 'Ошибка'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_type = models.CharField(max_length=50)
    input_data = models.JSONField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    result = models.JSONField(null=True, blank=True)
    error = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Task {self.id} ({self.task_type})"

