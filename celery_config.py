from celery import Celery

app = Celery(
    'tasks',  # Имя приложения Celery
    broker='redis://localhost:6379/0',  # Очередь задач (Redis)
    backend='redis://localhost:6379/0'  # Хранилище результатов выполнения задач
)

app.conf.task_always_eager = True  # Для тестирования, чтобы задачи выполнялись синхронно
