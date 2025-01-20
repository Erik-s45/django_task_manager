import time

from celery import shared_task

from .models import Task


@shared_task()
def process_task(task_id: int):
    """Функция выполнения задач в celery и обновления статусов выполнения."""
    task = Task.objects.get(pk=task_id)
    task.status = 'in_progress'
    task.save()
    try:
        if task.task_type == 'add':
            result = add(*task.input_data)
        elif task.task_type == 'wait':
            result = wait(*task.input_data)
        else:
            raise Exception(f'Неизвестный тип задачи: {task.task_type}')
    except Exception as e:
        task.status = 'error'
        task.error = [str(e)]
        task.save()
        return
    task.status = 'completed'
    task.result = [str(result)]
    task.save()


def add(a: int, b: int) -> int:
    """Функция сложения для выполнения в celery."""
    return a + b


def wait(s: int) -> str:
    """Функция отсчета секунд для выполнения в celery."""
    time.sleep(s)
    return f'Отсчет окончен: {s} секунд'
