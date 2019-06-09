from celery import shared_task
from django.conf import settings

from telegramapp.utils import cutretelegram_enviar_mensaje
from .models import Usuario


@shared_task
def expulsar_todos(canal_telegram=settings.TELEGRAM_GRUPO_LOG):
    gente_dentro = Usuario.objects.filter(estado=Usuario.DENTRO)
    gente_dentro_comas = ",".join(str(usuario.username) for usuario in gente_dentro)
    cutretelegram_enviar_mensaje("'{}' > ATPC".format(gente_dentro_comas), canal_telegram)
    gente_dentro.update(estado=Usuario.FUERA)
