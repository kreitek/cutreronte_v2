from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
import operator

from cutreronte.models import Dispositivo
from sniffer.models import RegistroMac


@login_required
def sniffer1(request):
    # registros = RegistroMac.objects.all()
    detectados = []

    for dispositivo in Dispositivo.objects.filter(usuario__isnull=True, equipo__isnull=True):  # solo anonimos
        # print("-----")
        estado_anterior = RegistroMac.FUERA
        tiempo_anterior = timezone.datetime.strptime('01/01/2019', "%m/%d/%Y")
        for registro in RegistroMac.objects.filter(dispositivo=dispositivo).order_by('tiempo'):
            estado = registro.estado
            tiempo = registro.tiempo
            # print("{}\t{}\t{}".format(registro, estado, tiempo))
            if estado == RegistroMac.FUERA and estado_anterior == RegistroMac.DENTRO:
                tiempo_dentro = tiempo - tiempo_anterior
                if tiempo_dentro > timezone.timedelta(seconds=settings.SNIFFER_TIMEOUT_SENAL * 2):
                    # print("=====> {}\t{}".format(tiempo_dentro, registro))
                    # detectados.append((registro, tiempo_dentro, tiempo))
                    detectados.append({"dispositivo_id": dispositivo.id,
                                       "mac": dispositivo.mac,
                                       "fabricante": dispositivo.fabricante,
                                       "tiempo_dentro": tiempo_dentro,
                                       "hora_salida": tiempo,
                                       "hora_entrada": tiempo_anterior,
                                       })
            estado_anterior = estado
            tiempo_anterior = tiempo

    # detectados.sort(key=operator.itemgetter(1), reverse=True)
    detectados.sort(key=operator.itemgetter("tiempo_dentro"), reverse=True)

    context = {
        'detectados': detectados,
    }
    return render(request, 'sniffer/sniffer.html', context)
