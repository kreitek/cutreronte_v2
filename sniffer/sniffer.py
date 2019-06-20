import threading
from django.conf import settings
from cutreronte.models import Dispositivo, Usuario
from sniffer.models import RegistroMac
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
        self.conectado = False
        self._TIEMPO_RECARGAR_MACS = 300
        self.macs_conocidas = []  # macs que estan asignadas a algun usuario
        self.running = False

    def run(self):
        if self.running:  # reiniciar
            self.stop()
        self.running = True
        self._recargar_macs_conocidas()
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
        if self.conectado:
            self.ser.close()
            self.conectado = False
        if self.running:
            self.timer.cancel()
            self.timer_recargar_macs.cancel()
        self.running = False

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
            usuario.meter()

    def _registrar_salida(self, mac):
        dispositivo, es_nuevo = Dispositivo.objects.get_or_create(mac=mac)
        RegistroMac.objects.create(dispositivo=dispositivo, estado=RegistroMac.FUERA)
        print("{} ha salido".format(mac))
        if mac in self.macs_conocidas:
            usuario = Usuario.objects.filter(dispositivo=dispositivo).first()
            usuario.sacar()

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

    def _recargar_macs_conocidas(self):
        """ Recarga el listado de MACs asignadas a algun usuario, cada cierto tiempo"""
        qs = Dispositivo.objects.filter(usuario__isnull=False)
        self.macs_conocidas = list(qs.values_list('mac', flat=True))
        self.timer_recargar_macs = threading.Timer(self._TIEMPO_RECARGAR_MACS, self._recargar_macs_conocidas)
        self.timer_recargar_macs.start()


def leer_todo_lo_que_viene(puerto, baudrate):
    ser = serial.Serial(puerto, baudrate, timeout=0.5)
    try:
        while True:
            if ser.inWaiting() > 0:
                response = ser.read_until()  # terminator=LF, size=None Read until a termination sequence is found ('\n' by default), the sizeis exceeded or until timeout occurs.
                response = response.decode('utf-8').strip()
                print(response)
    except (KeyboardInterrupt, SystemExit):
        ser.close()


if __name__ == '__main__':
    leer_todo_lo_que_viene("/dev/ttyUSB0", 115200)
