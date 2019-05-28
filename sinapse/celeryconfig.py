from celery import Celery
from decouple import config


app = Celery(
    config('BROKER_QUEUE', 'conexao-dev'),
    broker=config('BROKER_URL', default='redis://localhost:6379')
)
app.conf.timezone = 'UTC'
