import threading

from django.conf import settings

from apirest.models import RegistroMac
from cutreronte.models import Dispositivo, Usuario

import json
import redis
import serial
import time



SENAL_ENTRADA = 20


class SITUACION:
    DENTRO = 1
    FUERA = 0


class Sniffer:
    def __init__(self):
        self.redis_db = redis.StrictRedis(host="localhost", port=6379, db=12)
        self._vaciar_redis()
        self.conectado = False
        qs = Dispositivo.objects.filter(usuario__isnull=False)
        self.macs_conocidas = list(qs.values_list('mac', flat=True))
        self.running = False


    def run(self):
        if self.running:  # reiniciar
            self.stop()
        self.running = True
        self.timer = threading.Timer(10, self._reiniciar_senal)
        self.timer.start()
        while self.running:
            try:
                if not self.conectado:
                    self._conectar_serie()
                self._recibir_serie()
            except (serial.serialutil.SerialException, OSError):
                self.conectado = False
            # except (KeyboardInterrupt, SystemExit):
            #     break
            time.sleep(0.1)

    def stop(self):
        self.running = False
        if self.conectado:
            self.ser.close()
            self.conectado = False
        self.timer.cancel()

    def _recibir_serie(self):
        while self.ser.inWaiting() > 0:
            response = self.ser.read_until()  # terminator=LF, size=None Read until a termination sequence is found ('\n' by default), the sizeis exceeded or until timeout occurs.
            response = response.decode('utf-8').strip()
            if response.startswith("CLIENT,"):
                # print(response)
                partes = response.split(",")
                mac = partes[1]
                beacon = partes[2]
                canal = int(partes[3])
                senal = -int(partes[4])
                self._dispositivo_detectado(mac, senal, canal, beacon)

    def _conectar_serie(self):
        try:
            self.ser.close()
        except:
            pass
        while not self.conectado:
            try:
                self.ser = serial.Serial(settings.SNIFFER_SERIE_PUERTO, settings.SNIFFER_SERIE_BAUDRATE, timeout=0.5)
                self.conectado = True
            except:
                print("ERROR no se pudo abrir el puerto {}. Reintentando...".format(settings.SNIFFER_SERIE_PUERTO))
                time.sleep(10)



    def _dispositivo_detectado(self, mac, senal, canal, beacon):
        dispositivo = self.redis_db.get(mac)
        situacion = SITUACION.FUERA
        if dispositivo is None:
            print("Nuevo dispositivo {}, canal {}, señal {}".format(mac, canal, senal))
            if senal >= SENAL_ENTRADA:
                situacion = SITUACION.DENTRO
                self._registrar_entrada(mac)
        else:
            pl = json.loads(dispositivo.decode('utf-8'))
            anterior_senal = pl[0]
            anterior_canal = pl[1]
            anterior_tiempo = pl[2]
            situacion = pl[3]

            if situacion == SITUACION.FUERA and senal >= SENAL_ENTRADA:
                situacion = SITUACION.DENTRO
                self._registrar_entrada(mac)
                # print("Dispositivo reconectado {}, canal {}, señal {}".format(mac, canal, senal))
        tiempo = int(time.time())
        self.redis_db.set(mac, json.dumps([senal, canal, tiempo, situacion, beacon]))
        if mac in self.macs_conocidas:
            print("CONOCIDO {} , canal {}, señal {}, beacon {}".format(mac, canal, senal, beacon))


    def _registrar_entrada(self, mac):
        dispositivo, es_nuevo = Dispositivo.objects.get_or_create(mac=mac)
        RegistroMac.objects.create(dispositivo=dispositivo, estado=RegistroMac.DENTRO)
        print("{} ha entrado".format(mac))
        if mac in self.macs_conocidas:
            usuario = Usuario.objects.filter(dispositivo=dispositivo).first()
            usuario.estado = Usuario.DENTRO
            usuario.save()


    def _registrar_salida(self, mac):
        dispositivo, es_nuevo = Dispositivo.objects.get_or_create(mac=mac)
        RegistroMac.objects.create(dispositivo=dispositivo, estado=RegistroMac.FUERA)
        print("{} ha salido".format(mac))
        if mac in self.macs_conocidas:
            usuario = Usuario.objects.filter(dispositivo=dispositivo).first()
            usuario.estado = Usuario.FUERA
            usuario.save()


    def _vaciar_redis(self):
        for key in self.redis_db.keys():
            self.redis_db.delete(key)


    def _reiniciar_senal(self):
        """ Si no llega señal en un periodo de tiempo, la pasa a 0"""
        for mac in self.redis_db.keys():
            pl = json.loads(self.redis_db.get(mac).decode('utf-8'))
            senal = pl[0]
            canal = pl[1]
            tiempo = pl[2]
            situacion = pl[3]
            beacon = pl[4]
            ahora = time.time()
            if situacion == SITUACION.DENTRO and ahora - tiempo > settings.SNIFFER_TIMEOUT_SENAL:
                self.redis_db.set(mac, json.dumps([0, canal, ahora, SITUACION.FUERA, beacon]))
                mac_str = mac.decode('utf-8')
                self._registrar_salida(mac_str)
        self.timer = threading.Timer(10, self._reiniciar_senal)
        self.timer.start()

#
# def print_estadisticas(redis_db):
#     n_total = 0
#     n_dentro = 0
#     for mac in redis_db.keys():
#         n_total +=1
#         pl = json.loads(redis_db.get(mac).decode('utf-8'))
#         senal = pl[0]
#         canal = pl[1]
#         tiempo = pl[2]
#         situacion = pl[3]
#         beacon = pl[4]
#
#         if situacion == SITUACION.DENTRO:
#             n_dentro +=1
#     print("{} dispositivos en total. {} dentro.".format(n_total, n_dentro))
#
#
#
# def print_redis(redis_db, corte=0):
#     n_dispositivos = 0
#     for key in redis_db.keys():
#         try:
#             pl = json.loads(redis_db.get(key).decode('utf-8'))
#             mac = key.decode('utf-8')
#             senal = pl[0]
#             canal = pl[1]
#             tiempo = pl[2]
#             situacion = pl[3]
#             beacon = pl[4]
#             if senal > corte:
#                 print("{} {} {} {}".format(mac, senal, canal, tiempo))
#                 n_dispositivos += 1
#         except:
#             redis_db.delete(key)
#     print("numero de dispositivos: {}".format(n_dispositivos))
#
#
# def leer_todo_lo_que_viene(ser):
#     try:
#         while True:
#             if ser.inWaiting() > 0:
#
#                 response = ser.read_until()  # terminator=LF, size=None Read until a termination sequence is found ('\n' by default), the sizeis exceeded or until timeout occurs.
#                 response = response.decode('utf-8').strip()
#                 print(response)
#     except (KeyboardInterrupt, SystemExit):
#         ser.close()
#
#




if __name__ == '__main__':
    # leer_todo_lo_que_viene(ser)
    pass