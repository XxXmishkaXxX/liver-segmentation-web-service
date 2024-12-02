from __future__ import absolute_import, unicode_literals

# Это гарантирует, что приложение Celery будет загружено, когда Django загружает приложение
from .celery import app as celery_app

__all__ = ('celery_app',)
