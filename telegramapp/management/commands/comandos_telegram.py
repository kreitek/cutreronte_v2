from django.core.management.base import BaseCommand
from telegramapp.tasks import COMANDOS_TELEGARM_DISPONIBLES


class Command(BaseCommand):
    help = u'Para actualizar los comandos del bot de telegram'

    def handle(self, *args, **kwargs):
        respuesta = ""
        for key in COMANDOS_TELEGARM_DISPONIBLES.keys():
            if COMANDOS_TELEGARM_DISPONIBLES[key][1]:
                respuesta += "{} - {}\n".format(key, COMANDOS_TELEGARM_DISPONIBLES[key][1])
        print ("- Desde telegram llama a @BotFather\n- /setcommands\n- Selecciona el bot\n"
               "- Copia y pega:\n{}".format(respuesta[:-1]))
