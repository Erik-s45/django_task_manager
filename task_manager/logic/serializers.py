from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Task


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей"""
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор для создания задач и выведения списка задач."""
    class Meta:
        model = Task
        fields = ['id', 'user', 'task_type', 'input_data', 'status', 'created_at']
        read_only_fields = ['user', 'status', 'created_at']


class TaskDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для выведения полных данных о конкретной задаче."""
    class Meta:
        model = Task
        fields = '__all__'