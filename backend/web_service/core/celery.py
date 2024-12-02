from __future__ import absolute_import, unicode_literals
import os
from celery import Celery 

# Устанавливаем настройки для Celery из настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Загружаем задачи из всех зарегистрированных приложений Django
app.autodiscover_tasks()
