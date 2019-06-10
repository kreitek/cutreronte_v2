from django.core.management.base import BaseCommand
from cutreronte.models import Usuario, Rfid
import os


class Command(BaseCommand):
    help = u'Importa registros de cutreronte v1'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('filename', nargs='+', type=str)

        # Named (optional) arguments
        # parser.add_argument(
        #     '--delete',
        #     action='store_true',
        #     help='Delete poll instead of closing it',
        # )

    def handle(self, *args, **kwargs):
        filename = kwargs.get('filename')[0]
        os.stat(filename)  # lanza FileNotFoundError si no existe
        n_registros = 0
        with open(filename, 'r') as csv_file:
            # lineas = csv_file.readlines()
            for linea in csv_file:
                partes = linea.split(",")
                if len(partes) != 3:
                    raise ValueError(
                        "Fichero mal formado. El fichero tiene que ser un csv con y valores separados por coma: nombre, rfid y autorizado")
                try:
                    nombre_compuesto = partes[0].split("@")
                    nombre = nombre_compuesto[0].strip()
                    usuario_telegram = nombre_compuesto[1].strip()
                except:
                    nombre = partes[0].strip()
                    usuario_telegram = None
                nombre = nombre.replace("_", " ").title()
                if nombre == "None":
                    continue
                rfid = partes[1]
                autorizado = bool(partes[2])
                print("{} - {} - {} - {}".format(nombre, usuario_telegram, rfid, autorizado))
                try:
                    usuario = Usuario.objects.create(username=nombre, usuario_telegram=usuario_telegram,
                                                     autorizado=autorizado)
                except:
                    print("{} ya existe".format(nombre))
                    continue
                obj_rfid, _ = Rfid.objects.get_or_create(rfid=rfid)
                obj_rfid.usuario = usuario
                obj_rfid.save()
                n_registros += 1
        print("Importacion completada. Se han guardado {} registros".format(n_registros))
