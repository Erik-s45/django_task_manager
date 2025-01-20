# Task Manager API

## Установка

1. Склонируйте репозиторий `git clone https://github.com/Erik-s45/django_task_manager`
2. Создайте виртуальное окружение: `python -m venv venv`
3. Активируйте виртуальное окружение:
   - На Windows: `venv\Scripts\activate`
   - На macOS и Linux: `source venv/bin/activate`
4. Установите зависимости: `pip install -r requirements.txt`
5. Запустите Redis: `redis-server`
6. Запустите Celery: `celery -A task_manager worker --pool=solo -l info`
7. Запустите сервер: `python manage.py runserver`

## Эндпоинты

- `POST /api/register/` — Регистрация пользователя.
- `POST /api/token/` — Получение JWT токена.
- `POST /api/tasks/` — Создание задачи.
Типы задач: `add` - сложение двух чисел и `wait` - отсчет заданного количества секунд. 
Для корректной работы в `input_data` необходимо ввести значения в списке. 
Например, `task_type='add', input_data=[1, 2]` либо `task_type='wait', input_data=[20]`.
- `GET /api/tasks/` — Список задач пользователя с пагинацией и фильтрацией по статусу задачи.
Статусы задач: `scheduled` - запланирована, `in_progress` - выполняется, `completed` - завершена, `error` - ошибка.
- `GET /api/tasks/<task_id>/` — Детальная информация о задаче, включая результаты и ошибки.