from django.core.management.base import BaseCommand

from sniffer.sniffer import Sniffer


class Command(BaseCommand):
    help = u'Lanza servicio telegram'

    def handle(self, *args, **kwargs):
        print("Sniffer iniciado")
        sniffer = Sniffer()
        try:
            sniffer.run()
        except KeyboardInterrupt:
            sniffer.stop()
            print("Sniffer detenido")
            quit(0)
