from django.core.management.base import BaseCommand
from telegramapp import telegramapp


class Command(BaseCommand):
    help = u'Lanza servicio telegram'

    def handle(self, *args, **kwargs):
        print("Servicio Telegram iniciado")
        try:
            telegramapp.updater.idle()
        except KeyboardInterrupt:
            print("Servicio Telegram detenido")
            quit(0)
