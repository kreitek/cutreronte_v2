from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
import operator

from cutreronte.models import Dispositivo
from sniffer.models import RegistroMac


@login_required
def sniffer1(request):
    if request.POST:
        fecha = request.POST.get('fecha')
        print(fecha)
    else:
        fecha = timezone.datetime.now().strftime("%m/%d/%Y") #  06/14/2019
    mes, dia, anyo = fecha.split("/")
    detectados = []

    for dispositivo in Dispositivo.objects.filter(usuario__isnull=True, equipo__isnull=True):  # solo anonimos
        # print("-----")
        estado_anterior = RegistroMac.FUERA
        tiempo_anterior = timezone.datetime.strptime('01/01/2019', "%m/%d/%Y")
        for registro in RegistroMac.objects.filter(dispositivo=dispositivo, tiempo__year=anyo,
                      tiempo__month=mes, tiempo__day=dia).order_by('tiempo'):
            estado = registro.estado
            tiempo = registro.tiempo
            # print("{}\t{}\t{}".format(registro, estado, tiempo))
            if estado == RegistroMac.FUERA and estado_anterior == RegistroMac.DENTRO:
                tiempo_dentro = tiempo - tiempo_anterior
                if tiempo_dentro > timezone.timedelta(seconds=settings.SNIFFER_TIMEOUT_SENAL * 2):
                    # print("=====> {}\t{}".format(tiempo_dentro, registro))
                    # detectados.append((registro, tiempo_dentro, tiempo))
                    tiempo_dentro = tiempo_dentro - timezone.timedelta(microseconds=tiempo_dentro.microseconds)
                    hora_salida = tiempo - timezone.timedelta(seconds=settings.SNIFFER_TIMEOUT_SENAL)
                    detectados.append({"dispositivo_id": dispositivo.id,
                                       "mac": dispositivo.mac,
                                       "fabricante": dispositivo.fabricante,
                                       "tiempo_dentro": tiempo_dentro,  # timedelta
                                       "hora_salida": hora_salida,
                                       "hora_entrada": tiempo_anterior,
                                       })
            estado_anterior = estado
            tiempo_anterior = tiempo

    # detectados.sort(key=operator.itemgetter(1), reverse=True)
    detectados.sort(key=operator.itemgetter("tiempo_dentro"), reverse=True)
    context = {
        'fecha': fecha,
        'detectados': detectados,
    }
    return render(request, 'sniffer/sniffer.html', context)
