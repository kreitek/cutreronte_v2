import pytz
from celery import shared_task
from django.conf import settings
from django.utils import timezone
import redis

from .models import RegistroMac


@shared_task
def mantenimiento():
    borrar_registros_antiguos()
    vaciar_redis()


def borrar_registros_antiguos():
    ahora = timezone.datetime.now(pytz.timezone(settings.TIME_ZONE))
    hace_un_tiempo = ahora - timezone.timedelta(weeks=4)
    RegistroMac.objects.filter(tiempo__lte=hace_un_tiempo).delete()


def vaciar_redis():
    redis_db = redis.StrictRedis(host="localhost", port=6379, db=12)
    for key in redis_db.keys():
        redis_db.delete(key)
