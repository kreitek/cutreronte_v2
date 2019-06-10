from celery import shared_task
from django.conf import settings

from telegramapp.models import GrupoTelegram
from telegramapp.utils import cutretelegram_enviar_mensaje
from .models import Usuario


@shared_task
def expulsar_todos(notificar_telegram=True):
    gente_dentro = Usuario.objects.filter(estado=Usuario.DENTRO)
    gente_dentro_comas = ",".join(str(usuario.username) for usuario in gente_dentro)
    if gente_dentro and notificar_telegram:
        grupos_telegram = GrupoTelegram.objects.filter(notificar_cambios=True)
        for grupo in grupos_telegram:
            cutretelegram_enviar_mensaje("'{}' > ATPC".format(gente_dentro_comas), grupo.id_grupo)
    gente_dentro.update(estado=Usuario.FUERA)
    return gente_dentro_comas