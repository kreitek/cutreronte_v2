import os
from celery import Celery
from django.conf import settings
from celery.task.schedules import crontab


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cutreronte_v2.settings')
app = Celery('cutreronte_v2', backend='redis://localhost')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

# autodiscover tasks in any app
app.autodiscover_tasks(settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# set schedule
# from parker.apps.interactions.schedule import SCHEDULE
# app.conf.CELERYBEAT_SCHEDULE = SCHEDULE

# @periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
# def notificar_resumen_noche():
#     # from cutreronte_v2.telegram import bot
#     print("hola")

app.conf.beat_schedule = {
    'borrar-registro-macs-antiguas': {
        'task': 'sniffer.tasks.borrar_registros_antiguos',
        'schedule': crontab(hour="4", minute="0", day_of_week="*"),
        # 'args': ("uno dos", '46167421'),
    },
    'expulsar-gente-noche': {
        'task': 'cutreronte.tasks.expulsar_todos',
        'schedule': crontab(hour="1", minute="0", day_of_week="*"),
    },
}
