import pytz
from celery import shared_task
from django.conf import settings
from django.utils import timezone

from .models import RegistroMac


@shared_task
def borrar_registros_antiguos():
    ahora = timezone.datetime.now(pytz.timezone(settings.TIME_ZONE))
    hace_un_tiempo = ahora - timezone.timedelta(weeks=4)
    RegistroMac.objects.filter(tiempo__lte=hace_un_tiempo).delete()
