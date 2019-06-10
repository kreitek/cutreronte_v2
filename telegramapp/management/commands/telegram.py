from django.core.management.base import BaseCommand
from telegramapp import telegram


class Command(BaseCommand):
    help = u'Lanza servicio telegram'

    def handle(self, *args, **kwargs):
        print("Servicio Telegram iniciado")
        try:
            telegram.updater.idle()
        except KeyboardInterrupt:
            print("Servicio Telegram detenido")
            quit(0)
